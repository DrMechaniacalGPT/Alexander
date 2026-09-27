"""Finite scenarios; each completed turn is a durable replayable transaction."""
import argparse
import hashlib
import fcntl
import json
import random
import time
from pathlib import Path
from . import __version__
from .core import State, messages_for
from .models import Ollama, Stub
from .audit import violations


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    temp.replace(path)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def encounters(scene, players, rng):
    if scene.get('mode', 'fixed') == 'fixed':
        yield from scene['encounters']
    elif scene.get('mode') == 'random_pairs':
        for window in range(scene['windows']):
            available = [p for p in players if p not in scene.get('absent', [])]
            rng.shuffle(available)
            for i in range(0, len(available)-1, 2):
                yield {'participants': available[i:i+2], 'turns_each': scene.get('turns_each', 1),
                       'instruction': scene.get('instruction', 'Talk about what matters to you.'),
                       'window': window}


def report(state, out, status, manifest, failure=None):
    records = [json.loads(p.read_text()) for p in sorted((out/'turns').glob('*.json'))]
    attempts = [a for r in records for a in r.get('attempts', [])]
    usage = {'requests': len(attempts), 'new_requests': sum(len(r.get('attempts', [])) for r in records if not r.get('inherited_from')), 'inherited_turns': sum(bool(r.get('inherited_from')) for r in records), 'wall_seconds': round(sum(a.get('result', {}).get('wall_seconds', 0) for a in attempts), 3),
             'prompt_tokens': sum(a.get('result', {}).get('response', {}).get('prompt_eval_count', 0) for a in attempts),
             'output_tokens': sum(a.get('result', {}).get('response', {}).get('eval_count', 0) for a in attempts)}
    limit_hits = []
    for r in records:
        for field, rule in r.get('request', {}).get('format', {}).get('properties', {}).items():
            value = r.get('accepted', {}).get(field)
            if isinstance(value, str) and 'maxLength' in rule and len(value) >= rule['maxLength']:
                limit_hits.append({'turn': r['key'], 'field': field, 'length': len(value)})
    summary = {'status': status, 'failure': failure, 'scenario': state.case['id'],
               'manifest': manifest, 'usage': usage, 'field_limit_hits': limit_hits, 'events': len(state.events),
               'contacts': {p: sorted(v) for p, v in state.contacts.items()},
               'transitions': getattr(state, 'transitions', []),
               'conclusions': state.conclusions, 'actions': state.actions,
               'limitation': 'Synthetic participants; delivery is not belief. No human validity claim.'}
    dump(out/'summary.json', summary)
    dump(out/'events.json', state.events)
    for pid in state.case['players']:
        # Full delivered history for inspection, not the bounded model context.
        dump(out/'players'/f'{pid}.json', {'role': state.case['players'][pid],
             'delivered': [e for e in state.events if pid in e['recipients']],
             'private': state.private[pid], 'conclusion': state.conclusions.get(pid)})
    text = [f"# {state.case['id']}", '', f'Status: **{status}**', '',
            f"Requests: {usage['requests']}; model wall time: {usage['wall_seconds']}s.",
            '', 'This is a simulated trace, not evidence of human enjoyment.', '', '## Conversations', '']
    for e in state.events:
        text.append(f"- `{e['id']}` {e['actor']} → {', '.join(e['recipients'])} ({e['scene']}, {e['kind']}): {e['content']}")
    text += ['', '## Private final conclusions', '']
    text += [f'- **{p}:** {c}' for p, c in state.conclusions.items()]
    if limit_hits: text += ['', 'Output fields at their schema limit (inspect for clipped meaning): '+json.dumps(limit_hits)]
    if failure: text += ['', 'Failure: '+failure]
    (out/'report.md').write_text('\n'.join(text)+'\n')
    return summary


def _run(case, out, backend, config, replay=False, continue_from=None, reuse_turns=None):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    manifest = {'engine': __version__, 'case_sha256': digest(case), 'config': config}
    if reuse_turns is not None and (continue_from is None or reuse_turns < 0):
        raise ValueError('reuse_turns requires a parent and a nonnegative count')
    parent = None
    if continue_from is not None:
        parent = Path(continue_from).resolve()
        if parent == out.resolve(): raise ValueError('Continuation needs a distinct output directory')
        previous = json.loads((parent/'manifest.json').read_text())
        if previous['case_sha256'] != manifest['case_sha256'] or previous['engine'] != manifest['engine']:
            raise ValueError('Continuation requires the same case and engine contract')
        for key in ('seed', 'backend', 'model', 'thinking'):
            default = False if key == 'thinking' else None
            if previous['config'].get(key, default) != config.get(key, default):
                raise ValueError('Continuation cannot change '+key)
        manifest['continuation'] = {'parent': parent.name, 'manifest_sha256': digest(previous), 'reuse_turns': reuse_turns}
    mf = out/'manifest.json'
    if mf.exists():
        existing = json.loads(mf.read_text())
        if 'continuation' in existing:
            existing['continuation']['parent'] = Path(existing['continuation']['parent']).name
        if existing != manifest:
            raise ValueError('Resume/replay manifest mismatch; use a new output directory')
    if parent is not None and not mf.exists():
        for i, source_path in enumerate(sorted((parent/'turns').glob('*.json'))):
            if reuse_turns is not None and i >= reuse_turns: break
            prior = json.loads(source_path.read_text())
            if not prior.get('accepted'): break
            prior['inherited_from'] = str(source_path)
            dump(out/'turns'/source_path.name, prior)
    dump(mf, manifest)
    state = State(case)
    rng = random.Random(config['seed'])
    start = time.monotonic(); counter = 0
    budget_file = out/'budget.json'
    budget = json.loads(budget_file.read_text()) if budget_file.exists() else {'requests': 0, 'elapsed': 0}
    # Count persisted attempts conservatively after an interruption between journal and budget writes.
    recorded_attempts = sum(len(json.loads(p.read_text()).get('attempts', [])) for p in (out/'turns').glob('*.json'))
    budget['requests'] = max(budget['requests'], recorded_attempts)
    start_elapsed = budget['elapsed']

    def checkpoint_budget():
        if not replay:
            budget['elapsed'] = start_elapsed + time.monotonic()-start
            dump(budget_file, budget)

    def turn(pid, audience, scene, instruction, final=False, legal_actions=('none',)):
        nonlocal counter
        key = f't{counter:05d}'; counter += 1
        messages = messages_for(state, pid, audience, scene, instruction, final, legal_actions, config.get('prompt_profile', 'legacy'))
        payload = backend.payload(messages)
        path = out/'turns'/f'{key}.json'
        record = json.loads(path.read_text()) if path.exists() else {'key': key, 'player': pid, 'request': payload, 'attempts': []}
        if (record['request']['messages'] != messages if replay or record.get('inherited_from') else record['request'] != payload):
            raise ValueError('Recorded prompt does not match replay state at '+key)
        if record.get('accepted'):
            action = record['accepted']
            backed = json.loads(record['attempts'][-1]['result']['response']['message']['content'])
            if action != backed:
                raise ValueError('Accepted action differs from recorded model output at '+key)
            if config.get('strict_output'):
                errors = violations(record['request'], record['attempts'][-1]['result'])
                if errors: raise ValueError('Strict output contract: '+ '; '.join(errors))
            state.apply(key, pid, audience, action, scene, final, legal_actions)
            return
        if replay:
            raise ValueError('Cannot replay an incomplete turn '+key)
        # An existing raw successful generation can be validated after a crash without a new call.
        prior = record['attempts'][-1] if record['attempts'] else None
        if prior and 'result' in prior and not prior.get('invalid'):
            result = prior['result']
        else:
            elapsed = start_elapsed + time.monotonic()-start
            if budget['requests'] >= config['max_calls'] or elapsed >= config['max_seconds']:
                raise RuntimeError('Configured run budget reached; no new generation attempted')
            attempt = {'started': time.time()}
            record['attempts'].append(attempt)
            dump(path, record)
            budget['requests'] += 1; checkpoint_budget()
            try:
                result = backend.complete(payload, timeout=min(120, max(1, config['max_seconds']-elapsed)))
                attempt['result'] = result
            except Exception as exc:
                attempt['error'] = str(exc); dump(path, record)
                raise
            dump(path, record)
        try:
            raw = result['response']
            if raw.get('truncated') or raw.get('done_reason') == 'length':
                raise ValueError('Truncated generation; inspect raw output and explicitly revise limits')
            if config.get('strict_output'):
                errors = violations(payload, result)
                if errors: raise ValueError('Strict output contract: '+ '; '.join(errors))
            action = json.loads(raw['message']['content'])
            state.apply(key, pid, audience, action, scene, final, legal_actions)
        except Exception as exc:
            record['attempts'][-1]['invalid'] = str(exc); dump(path, record)
            raise
        record['accepted'] = action; dump(path, record)
        checkpoint_budget()
        print(json.dumps({'turn': key, 'player': pid, 'scene': scene,
                          'seconds': result.get('wall_seconds'), 'action': action['action']}), flush=True)

    failure = None
    try:
        for scene_num, scene in enumerate(case['scenes']):
            sid = scene.get('id', f's{scene_num}')
            state.present = set(case['players']) - set(scene.get('absent', []))
            scene_contacts = {p: set() for p in case['players']}
            action_start = len(state.actions)
            transition_reason = 'schedule_budget'
            condition = scene.get('transition_after_contacts')
            for n, delivery in enumerate(scene.get('deliveries', [])):
                recipients = sorted(set(delivery['recipients']) & state.present)
                state.emit(f'{sid}:d{n}', 'host', recipients, delivery['content'], sid, 'delivery')
            for ei, encounter in enumerate(encounters(scene, list(case['players']), rng)):
                members = encounter['participants']
                if not set(members) <= state.present:
                    raise ValueError('Scheduled an absent participant')
                speakers = encounter.get('speakers', members)
                if not set(speakers) <= set(members): raise ValueError('Speaker outside encounter')
                for _ in range(encounter.get('turns_each', 1)):
                    for pid in speakers:
                        turn(pid, members, sid, encounter.get('instruction', 'What do you say next?'),
                             legal_actions=encounter.get('legal_actions', ['none']))
                for pid in members:
                    scene_contacts[pid].update(set(members)-{pid})
                if condition and len(scene_contacts[condition['player']]) >= condition['count']:
                    transition_reason = 'contact_trigger'
                    break
            if not hasattr(state, 'transitions'): state.transitions = []
            state.transitions.append({'scene': sid, 'reason': transition_reason, 'contact_trigger': condition,
                'contact_count': len(scene_contacts[condition['player']]) if condition else None})
            required = scene.get('requires_action')
            if required and not any(a['actor']==required['player'] and a['action']==required['action'] for a in state.actions[action_start:]):
                raise ValueError('Prescribed action did not happen; cannot advance: '+str(required))
        # Private assessments: do not expose one player's answer to another.
        state.present = set(case['players'])
        for pid in case['players']:
            turn(pid, [pid], 'assessment', case.get('question', 'What have you concluded, and what remains uncertain?'), True)
        for ei, encounter in enumerate(case.get('epilogue', [])):
            epilogue_action_start = len(state.actions)
            for pid in encounter.get('speakers', encounter['participants']):
                turn(pid, encounter['participants'], 'epilogue', encounter['instruction'],
                     legal_actions=encounter.get('legal_actions', ['none']))
            expected = encounter.get('required_action')
            if expected and not any(a['action'] == expected and a['scene'] == 'epilogue' for a in state.actions[epilogue_action_start:]):
                raise ValueError('Prescribed epilogue action did not happen')
        for i, content in enumerate(case.get('reveal', [])):
            state.emit(f'reveal:{i}', 'host', list(case['players']), content, 'reveal', 'delivery')
        status = 'complete'
    except Exception as exc:
        failure = type(exc).__name__+': '+str(exc); status = 'incomplete'
    finally:
        checkpoint_budget()
    return report(state, out, status, manifest, failure)


def run(case, out, backend, config, replay=False, continue_from=None, reuse_turns=None):
    """Prevent concurrent writers; OS releases the lock after a killed process."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    with (out/'.run.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('This run directory is already active') from exc
        return _run(case, out, backend, config, replay, continue_from, reuse_turns)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('case', type=Path); p.add_argument('--out', type=Path, required=True)
    p.add_argument('--backend', choices=['stub','ollama'], default='stub')
    p.add_argument('--model', default='qwen3.5:9b'); p.add_argument('--seed', type=int, default=1)
    p.add_argument('--context', type=int, default=4096); p.add_argument('--tokens', type=int, default=256)
    p.add_argument('--max-calls', type=int, default=32); p.add_argument('--max-seconds', type=float, default=1800)
    p.add_argument('--prompt-profile', choices=['legacy','grounded-v1','grounded-v2','dialogue-v1'], default='legacy')
    p.add_argument('--thinking', action='store_true', help='Enable local model reasoning; budget enough output tokens')
    p.add_argument('--strict-output', action='store_true', help='Constrain phase-specific fields and reject violations')
    p.add_argument('--replay', action='store_true')
    p.add_argument('--reuse-turns', type=int, help='Limit inherited accepted prefix when explicitly revising later prompts')
    p.add_argument('--continue-from', type=Path, help='Explicitly reuse a compatible accepted prefix in a new run directory')
    args = p.parse_args()
    case = json.loads(args.case.read_text())
    config = {k:v for k,v in vars(args).items() if k not in ('case','out','replay','continue_from','reuse_turns')}
    if config['prompt_profile'] == 'legacy':
        del config['prompt_profile']  # Preserve historical manifest and replay compatibility.
    for key in ('thinking', 'strict_output'):
        if not config[key]: del config[key]  # Historical manifests omit these options.
    backend = Ollama(args.model, context=args.context, tokens=args.tokens, seed=args.seed, thinking=args.thinking, strict_output=args.strict_output) if args.backend=='ollama' else Stub(case.get('stub', {}), strict_output=args.strict_output)
    summary = run(case, args.out, backend, config, args.replay, args.continue_from, args.reuse_turns)
    print(json.dumps({k:summary[k] for k in ('status','failure','usage')}, indent=2))
    raise SystemExit(0 if summary['status']=='complete' else 1)

if __name__ == '__main__': main()
