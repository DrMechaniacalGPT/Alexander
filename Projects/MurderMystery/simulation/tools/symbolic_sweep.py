"""Run from any directory; emits compact JSON summary and optional JSONL traces."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dojo.symbolic import simulate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fixture', type=Path)
    parser.add_argument('--seeds', default='1,2,3,4,5')
    parser.add_argument('--partners', default='0,1,2,3')
    parser.add_argument('--packets', type=int, default=2)
    parser.add_argument('--relay', action='store_true')
    parser.add_argument('--include-culprit', action='store_true', help='Include privileged culprit decisions in scores')
    parser.add_argument('--group-rounds', type=int, default=0)
    parser.add_argument('--group-packets', type=int, default=2)
    parser.add_argument('--trace', type=Path, help='Optional full results JSONL; may contain private facts')
    args = parser.parse_args()
    game = json.loads(args.fixture.read_text())
    seeds = [int(x) for x in args.seeds.split(',')]
    partners = [int(x) for x in args.partners.split(',')]
    if len(set(seeds)) != len(seeds):
        parser.error('Seeds must be distinct')
    handle = args.trace.open('w') if args.trace else None
    summaries = []
    try:
        for count in partners:
            correct = guesses = unique = fallback = 0
            for seed in seeds:
                result = simulate(game, count, seed, args.packets, args.relay,
                                  args.group_rounds, args.group_packets)
                scored = [p for p in game['players'] if args.include_culprit or p != game.get('truth', {}).get('culprit')]
                values = [result['decisions'][p] for p in scored]
                guesses += len(values)
                unique += sum(len(d['remaining']) == 1 for d in values)
                fallback += sum(d['guess_fallback'] for d in values)
                correct += sum(result['evaluation'].get('correct', {}).get(p, False) for p in scored)
                if handle:
                    handle.write(json.dumps({'partners': count, 'result': result}) + '\n')
            summaries.append({'partners': count, 'party_seeds': seeds, 'player_decisions': guesses,
                              'unique_remaining': unique, 'fallback_guesses': fallback,
                              'correct_required_guesses': correct if 'culprit' in game.get('truth', {}) else None})
    finally:
        if handle:
            handle.close()
    print(json.dumps({'settings': {'packets': args.packets, 'relay': args.relay,
                                  'group_rounds': args.group_rounds, 'group_packets': args.group_packets,
                                  'include_culprit': args.include_culprit},
                      'sweep': summaries}, indent=2))


if __name__ == '__main__':
    main()
