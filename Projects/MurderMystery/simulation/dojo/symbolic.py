"""Bounded, source-preserving fact sharing; no language model or hidden-answer access."""
import random

from .schedule import distinct_encounters


def prepare(scenario):
    """Validate input and canonicalize duplicate clue IDs without amplifying evidence."""
    players = list(scenario['players'])
    if len(players) < 2 or len(players) % 2 or len(set(players)) != len(players):
        raise ValueError('An even number of distinct players is required')
    packets = {}
    for fact in scenario.get('facts', []):
        if fact['owner'] not in players or fact['subject'] not in players:
            raise ValueError('Unknown fact owner or subject')
        assertions = fact.get('assertions')
        if assertions is None:
            assertions = [{k: fact[k] for k in ('predicate', 'value', 'source_atom')}]
        if not isinstance(assertions, list):
            raise ValueError('Assertions must be a list (possibly empty)')
        for assertion in assertions:
            if (type(assertion['value']) is not bool or not assertion['source_atom']
                    or not isinstance(assertion['predicate'], str)):
                raise ValueError('Assertions require a predicate, boolean and source atom')
        key = 'fact:' + fact['id']
        if key in packets:
            raise ValueError('Duplicate fact packet ID')
        packets[key] = dict(fact, kind='fact', assertions=[dict(item) for item in assertions])
    for clue in scenario.get('clues', []):
        if type(clue['expected']) is not bool or clue['strength'] not in ('hard', 'soft'):
            raise ValueError('Invalid clue')
        if not clue['source_atom'] or not set(clue['recipients']) <= set(players):
            raise ValueError('Invalid clue source or recipient')
        key = 'clue:' + clue['id']
        if key in packets:
            old = packets[key]
            comparable = ('predicate', 'expected', 'strength', 'source_atom')
            if any(old[field] != clue[field] for field in comparable):
                raise ValueError('Conflicting definitions of the same clue ID')
            old['recipients'] = sorted(set(old['recipients']) | set(clue['recipients']))
        else:
            packets[key] = dict(clue, kind='clue', recipients=list(clue['recipients']))
    for packet in packets.values():
        for assertion in packet.get("assertions", []):
            if not set(assertion.get("requires", [])) <= packets.keys():
                raise ValueError("Unknown prerequisite packet")
    return players, packets


def assess(players, packets, known, seed=1, private_exclusions=()):
    """Use only explicitly known packets. Unknown/conflicting facts never exclude."""
    known = set(known)
    if not known <= packets.keys():
        raise ValueError('Unknown packet ID')
    if not set(private_exclusions) <= set(players):
        raise ValueError('Unknown private exclusion')
    facts = [dict(assertion, id=packets[k]['id'], subject=packets[k]['subject'])
             for k in sorted(known) if packets[k]['kind'] == 'fact'
             for assertion in packets[k]['assertions']
             if set(assertion.get('requires', [])) <= known]
    clues = [packets[k] for k in sorted(known) if packets[k]['kind'] == 'clue']
    candidates = {}
    for player in players:
        predicates = sorted({f['predicate'] for f in facts if f['subject'] == player}
                            | {c['predicate'] for c in clues})
        states = {}
        for predicate in predicates:
            assertions = [f for f in facts if f['subject'] == player and f['predicate'] == predicate]
            values = {f['value'] for f in assertions}
            state = 'unknown' if not values else 'inconsistent' if len(values) > 1 else next(iter(values))
            states[predicate] = {'state': state, 'sources': sorted({f['source_atom'] for f in assertions}),
                                 'packets': sorted(f['id'] for f in assertions)}
        matches, contradictions, soft_matches, sources = [], [], [], set()
        for clue in clues:
            state = states[clue['predicate']]['state']
            if type(state) is not bool:
                continue
            if state == clue['expected']:
                if clue['strength'] == 'hard':
                    matches.append(clue['id'])
                    sources.update(states[clue['predicate']]['sources'])
                else:
                    soft_matches.append(clue['id'])
            elif clue['strength'] == 'hard':
                contradictions.append(clue['id'])
        candidates[player] = {
            'states': states, 'matches': matches, 'contradictions': contradictions,
            'soft_matches': soft_matches, 'supported_match_count': len(matches),
            'unique_source_match_count': len(sources),
            'private_excluded': player in private_exclusions,
        }
    remaining = [p for p in players if not candidates[p]['contradictions']
                 and not candidates[p]['private_excluded']]
    # Required choice: unknown-only candidates stay eligible, but matches rank support.
    pool = remaining or [p for p in players if p not in private_exclusions]
    if not pool:
        raise ValueError('Private exclusions leave no possible vote')
    best = max(candidates[p]['supported_match_count'] for p in pool)
    tied = sorted(p for p in pool if candidates[p]['supported_match_count'] == best)
    guess = random.Random(seed).choice(tied)
    return {'candidates': candidates, 'remaining': remaining, 'guess': guess,
            'guess_tied_candidates': tied, 'guess_fallback': not remaining,
            'guess_policy': 'max_hard_matches; seeded_tie; nonprivate_candidates_if_none_remain'}


def simulate(scenario, partners=1, seed=1, packets_per_encounter=2, relay=False,
             group_rounds=0, group_packets=2):
    """Share before clues, then private clues, then bounded synchronous broadcasts."""
    players, packets = prepare(scenario)
    for value in (packets_per_encounter, group_rounds, group_packets):
        if type(value) is not int or value < 0:
            raise ValueError('Budgets must be nonnegative integers')
    if type(partners) is not int or not 0 <= partners < len(players):
        raise ValueError('Invalid partner count')
    ledger = {p: {k for k, f in packets.items() if f['kind'] == 'fact' and f['owner'] == p}
              for p in players}
    for p, ids in scenario.get('initial_known', {}).items():
        if p not in ledger or not set(ids) <= packets.keys():
            raise ValueError('Invalid initial knowledge')
        if any(packets[k]['kind'] != 'fact' for k in ids):
            raise ValueError('Clues are delivered only after mingling')
        ledger[p].update(ids)
    trace = []
    rng = random.Random(seed)

    def choose(ids, limit):
        choices = sorted(ids)
        rng.shuffle(choices)
        return choices[:limit]

    schedule = distinct_encounters(players, partners, seed) if partners else []
    for index, encounter in enumerate(schedule):
        left, right = encounter['participants']
        # Compute BOTH selections before either delivery: no same-encounter cascade.
        sends = []
        for sender, receiver in ((left, right), (right, left)):
            available = {k for k in ledger[sender] - ledger[receiver]
                         if packets[k]['kind'] == 'fact'
                         and (relay or packets[k]['owner'] == sender)}
            sends.append((sender, receiver, choose(available, packets_per_encounter)))
        for sender, receiver, ids in sends:
            ledger[receiver].update(ids)
            trace.append({'phase': 'mingling', 'encounter': index, 'window': encounter['window'],
                          'sender': sender, 'recipients': [receiver], 'packets': ids})
    for key, packet in sorted(packets.items()):
        if packet['kind'] == 'clue':
            for recipient in packet['recipients']:
                ledger[recipient].add(key)
            trace.append({'phase': 'clues', 'sender': 'host', 'recipients': packet['recipients'],
                          'packets': [key]})
    for round_index in range(group_rounds):
        # Every speaker chooses from knowledge at the START of the round.
        snapshot = {p: set(ids) for p, ids in ledger.items()}
        sends = []
        for sender in players:
            available = {k for k in snapshot[sender]
                         if any(k not in snapshot[q] for q in players if q != sender)
                         and (packets[k]['kind'] == 'clue' or relay or packets[k]['owner'] == sender)}
            sends.append((sender, choose(available, group_packets)))
        for sender, ids in sends:
            recipients = [p for p in players if p != sender]
            for p in recipients:
                ledger[p].update(ids)
            trace.append({'phase': 'group', 'round': round_index, 'sender': sender,
                          'recipients': recipients, 'packets': ids})
    decisions = {p: assess(players, packets, ledger[p], seed + i,
                           scenario.get('private_exclusions', {}).get(p, []))
                 for i, p in enumerate(players)}
    reference = assess(players, packets, set(packets), seed)
    # Evaluator-only access happens after every transmission and decision is fixed.
    culprit = scenario.get('truth', {}).get('culprit')
    evaluation = {'culprit_supplied': culprit is not None}
    if culprit is not None:
        if culprit not in players:
            raise ValueError('Unknown evaluator culprit')
        evaluation['correct'] = {p: result['guess'] == culprit for p, result in decisions.items()}
    return {'seed': seed, 'schedule': schedule, 'trace': trace,
            'known_packets': {p: sorted(ids) for p, ids in ledger.items()},
            'decisions': decisions, 'full_information': reference, 'evaluation': evaluation}
