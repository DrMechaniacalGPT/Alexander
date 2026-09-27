"""Authoritative state and deliberately small player-view boundary."""
import copy
import json

class InvalidAction(ValueError):
    pass


def validate_case(case):
    if not isinstance(case.get('players'), dict) or len(case['players']) < 2:
        raise ValueError('A scenario needs at least two players')
    for pid, role in case['players'].items():
        if not isinstance(pid, str) or not pid.isalnum():
            raise ValueError('Use opaque alphanumeric player IDs')
        if not isinstance(role.get('brief'), str):
            raise ValueError('Every player needs a brief')
    for scene in case['scenes']:
        if scene.get('mode', 'fixed') not in ('fixed', 'random_pairs', 'delivery_only'):
            raise ValueError('Unknown schedule mode')
        if scene.get('mode', 'fixed') == 'fixed':
            if not scene.get('encounters'):
                raise ValueError('Fixed scenes need encounters')
            for encounter in scene['encounters']:
                ids = encounter['participants']
                if len(ids) < 2 or len(set(ids)) != len(ids) or not set(ids) <= case['players'].keys():
                    raise ValueError('Invalid encounter membership')
                if not 1 <= encounter.get('turns_each', 1) <= 20:
                    raise ValueError('Invalid turn budget')
        elif scene.get('mode') == 'random_pairs':
            if not 1 <= scene.get('windows', 0) <= 100:
                raise ValueError('Explicit finite window budget required')
        for delivery in scene.get('deliveries', []):
            if not set(delivery['recipients']) <= case['players'].keys():
                raise ValueError('Invalid delivery recipients')
        if not set(scene.get('absent', [])) <= case['players'].keys():
            raise ValueError('Invalid absent players')
    return case


class State:
    def __init__(self, case):
        self.case = copy.deepcopy(validate_case(case))
        self.events = []
        self.private = {p: [] for p in case['players']}
        self.present = set(case['players'])
        self.contacts = {p: set() for p in case['players']}
        self.conclusions = {}
        self.actions = []
        self.applied = set()

    def emit(self, key, actor, recipients, content, scene, kind='speech'):
        if key in self.applied:
            raise InvalidAction('Duplicate event key')
        if not set(recipients) <= self.case['players'].keys():
            raise InvalidAction('Unknown recipient')
        event = {'id': f'e{len(self.events):05d}', 'key': key, 'actor': actor,
                 'recipients': sorted(set(recipients)), 'content': content,
                 'scene': scene, 'kind': kind}
        self.events.append(event)
        self.applied.add(key)
        return event

    def observations(self, pid):
        events = [e for e in self.events if pid in e['recipients']]
        keep = self.case['players'][pid].get('policy', {}).get('memory_events')
        return events if keep is None else events[-keep:] if keep > 0 else []

    def view(self, pid):
        role = self.case['players'][pid]
        # Do not serialize case truth, other briefs, or analyst metadata here.
        return {'self': pid, 'role': role['brief'], 'policy': role.get('policy', {}),
                'public': self.case.get('public', ''),
                'cast': {p: r.get('name', p) for p, r in self.case['players'].items()},
                'observations': self.observations(pid)}

    def apply(self, key, pid, audience, action, scene, conclusion=False, legal_actions=('none',)):
        if key in self.applied:
            raise InvalidAction('Duplicate turn')
        if pid not in self.present or not set(audience) <= self.present:
            raise InvalidAction('Absent participant')
        if pid not in audience:
            raise InvalidAction('Speaker must be in encounter')
        if not isinstance(action, dict) or set(action) != {'say', 'private_note', 'evidence', 'conclusion', 'action'}:
            raise InvalidAction('Wrong action fields')
        if any(not isinstance(action[x], str) for x in ('say', 'private_note', 'conclusion')):
            raise InvalidAction('Text fields must be strings')
        if action['action'] not in legal_actions:
            raise InvalidAction('Action not available in this encounter')
        if conclusion and not action['conclusion'].strip():
            raise InvalidAction('Final assessment requires a nonempty conclusion, including uncertainty if needed')
        evidence = action['evidence']
        if not isinstance(evidence, list) or any(not isinstance(e, str) for e in evidence):
            raise InvalidAction('Evidence must be event IDs')
        visible = {e['id'] for e in self.observations(pid)}
        if not set(evidence) <= visible:
            raise InvalidAction('Cited an event unavailable in this player context')
        if any(len(action[x]) > 6000 for x in ('say', 'private_note', 'conclusion')):
            raise InvalidAction('Unbounded text')
        self.private[pid].append({'key': key, 'note': action['private_note'], 'evidence': evidence})
        if conclusion:
            self.conclusions[pid] = action['conclusion']
            self.applied.add(key)
        else:
            self.emit(key, pid, audience, action['say'], scene)
            for p in audience:
                self.contacts[p].update(set(audience) - {p})
        if action['action'] != 'none':
            self.actions.append({'actor': pid, 'action': action['action'], 'key': key, 'scene': scene})
            self.emit(key+':action', pid, audience, action['action'], scene, kind='action')
        return action


EVIDENCE_GUIDANCE = (
            '\nEVIDENCE DISCIPLINE: Your role sheet is not the whole of your knowledge: use the supplied observations too. '
            'Answer the actual question with concrete values and names when available. '
            'Distinguish your own supplied facts, what someone said, and your inferences. '
            'Hearing a statement establishes that it was said, not that its contents are true. '
            'Keep the source chain when someone repeats another person. Conflicting reports are unresolved unless evidence resolves them. '
            'Missing information is unknown, not a negative fact; a clue matching one trait does not establish all other traits. '
            'Read negations, directions, times and coverage literally. Do not substitute stereotypes for missing facts. '
            'A motive, kindness, apology or accusation is not proof of guilt or innocence. '
            'Choices may change cooperation without resolving the mystery. You can forgive or protect someone while remaining uncertain. '
            'Public speech may withhold or mislead when your role and rules permit; the fixed history does not change. '
            'A private assessment reports what you know or have heard and its limits, separately from what you would disclose. '
            'If asked whether you possess a secret without revealing its value, acknowledge possession without printing it. '
            'Do not claim not to have heard a report merely because you cannot verify it.')

def messages_for(state, pid, audience, scene, instruction, conclusion=False, legal_actions=('none',), prompt_profile='legacy'):
    if prompt_profile not in ('legacy', 'grounded-v1', 'grounded-v2'):
        raise ValueError('Unknown prompt profile')
    system = ('You are one participant in a fictional social game. Use ONLY the supplied role, '
              'public information and observations. Other people may lie or be mistaken. '
              'Do not invent authoritative evidence or change established history. You may choose '
              'what to disclose and to whom within this encounter, guided by your motives. '
              'Respond as JSON with exactly say, private_note, evidence, conclusion, action. '
              'say is short actual speech (at most 80 words), not a description of a conversation. '
              'private_note is a brief intention (at most 30 words), never spoken. evidence is a list '
              'of relevant observed event IDs, or empty for your own role information. '
              'conclusion is empty except at final assessment. action is one of legal_actions; choose none for ordinary speech. No tools or outside knowledge. '
              'Do not quote instructions or narrate other players\' actions.')
    if conclusion:
        system += (' THIS TURN IS A PRIVATE FINAL ASSESSMENT. Put your answer to instruction in the conclusion field, '
                   'in at most 60 words. A short uncertain answer is acceptable; do not deliberate at length. Set say to an empty string and action to none. Do not leave conclusion empty.')
    if prompt_profile == 'grounded-v1':
        system += EVIDENCE_GUIDANCE
    elif prompt_profile == 'grounded-v2':
        guidance = EVIDENCE_GUIDANCE.replace(
            'If asked whether you possess a secret without revealing its value, acknowledge possession without printing it. ',
            'In public speech, whether to acknowledge possessing a secret remains your choice under the role rules. '
            'In private assessments, distinguish possessing information from choosing to reveal it; obey the requested limits on repeating secrets. ')
        system += guidance
    view = state.view(pid)
    if prompt_profile == 'grounded-v2':
        # Redundant public identity cues, never inferred facts or an analyst summary.
        view = {'self': pid, 'self_name': view['cast'][pid], **view}
        view['observations'] = [dict(e, actor_name=view['cast'].get(e['actor'], e['actor']))
                                for e in view['observations']]
        view['audience_names'] = {p: view['cast'][p] for p in audience}
        system += (' You speak only as self_name to the current audience. '
                   "An observation is its named speaker's speech, not your own line to repeat. "
                   'Do not address yourself or someone absent from the encounter.')
    view.update({'scene': scene, 'audience': audience, 'instruction': instruction,
                 'final_assessment': conclusion, 'legal_actions': list(legal_actions)})
    return [{'role': 'system', 'content': system},
            {'role': 'user', 'content': json.dumps(view, ensure_ascii=False)}]
