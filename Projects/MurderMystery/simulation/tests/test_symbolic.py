import copy
import json
from pathlib import Path
import unittest

from dojo.symbolic import assess, prepare, simulate

FIXTURE = Path(__file__).resolve().parents[1] / 'fixtures/symbolic_museum.json'


class SymbolicTests(unittest.TestCase):
    def setUp(self):
        self.game = json.loads(FIXTURE.read_text())

    def test_unknown_false_and_conflict(self):
        self.game['facts'].append(dict(self.game['facts'][0], id='a-conflict', value=False, source_atom='another'))
        players, packets = prepare(self.game)
        result = assess(players, packets, ['clue:pet-clue', 'fact:a-pet'])
        self.assertNotIn('a', result['remaining'])
        self.assertIn('b', result['remaining'])  # Missing is not a match or exclusion.
        self.assertEqual(result['candidates']['b']['supported_match_count'], 0)
        result = assess(players, packets, ['clue:pet-clue', 'fact:a-pet', 'fact:a-conflict', 'fact:b-pet'])
        self.assertIn('a', result['remaining'])
        self.assertEqual(result['candidates']['a']['states']['has_pet']['state'], 'inconsistent')
        self.assertEqual(result['candidates']['b']['supported_match_count'], 1)

    def test_duplicates_and_sources(self):
        self.game['clues'].append(copy.deepcopy(self.game['clues'][0]))
        self.game['facts'].append(dict(self.game['facts'][2], id='b-copy'))
        players, packets = prepare(self.game)
        result = assess(players, packets, ['clue:pet-clue', 'fact:b-pet', 'fact:b-copy'])
        self.assertEqual(result['candidates']['b']['supported_match_count'], 1)
        self.assertEqual(result['candidates']['b']['unique_source_match_count'], 1)

    def test_isolation_and_private_clues(self):
        result = simulate(self.game, partners=0)
        self.assertEqual(set(result['known_packets']['a']), {'fact:a-pet', 'fact:a-wing', 'clue:pet-clue'})
        self.assertEqual(result['decisions']['a']['candidates']['b']['states']['has_pet']['state'], 'unknown')

    def test_snapshot_sends_no_immediate_cascade(self):
        result = simulate(self.game, partners=1, relay=True, packets_per_encounter=99)
        left, right = result['trace'][:2]
        self.assertTrue(left['packets'])
        self.assertTrue(set(left['packets']).isdisjoint(right['packets']))
        # Stronger check: every send is in sender's pre-encounter ledger.
        initial = {p: {'fact:' + f['id'] for f in self.game['facts'] if f['owner'] == p}
                   for p in self.game['players']}
        for send in result['trace']:
            if send['phase'] == 'mingling':
                self.assertLessEqual(set(send['packets']), initial[send['sender']])

    def test_complete_information_and_group_delivery(self):
        result = simulate(self.game, partners=3, packets_per_encounter=2, group_rounds=1, group_packets=99)
        self.assertEqual(result['full_information']['remaining'], ['b'])
        self.assertTrue(all(d['remaining'] == ['b'] for d in result['decisions'].values()))
        self.assertTrue(all(result['evaluation']['correct'].values()))

    def test_replay_and_truth_is_evaluator_only(self):
        first = simulate(self.game, partners=2, seed=73, relay=True, group_rounds=2)
        self.assertEqual(first, simulate(self.game, partners=2, seed=73, relay=True, group_rounds=2))
        self.game['truth']['culprit'] = 'd'
        second = simulate(self.game, partners=2, seed=73, relay=True, group_rounds=2)
        self.assertNotEqual(first.pop('evaluation'), second.pop('evaluation'))
        self.assertEqual(first, second)

    def test_soft_clue_and_exhausted_candidates(self):
        self.game['clues'][0]['strength'] = 'soft'
        players, packets = prepare(self.game)
        result = assess(players, packets, ['clue:pet-clue', 'fact:a-pet'])
        self.assertIn('a', result['remaining'])
        self.assertEqual(result['candidates']['a']['supported_match_count'], 0)
        with self.assertRaises(ValueError):
            assess(players, packets, [], private_exclusions=players)

    def test_fallback_does_not_accuse_privately_cleared_self(self):
        self.game['facts'] = [dict(id=p, owner=p, subject=p, predicate='x', value=False, source_atom=p) for p in self.game['players']]
        self.game['clues'] = [dict(id='x', predicate='x', expected=True, strength='hard', source_atom='clue', recipients=[])]
        players, packets = prepare(self.game)
        result = assess(players, packets, set(packets), private_exclusions=['a'])
        self.assertTrue(result['guess_fallback'])
        self.assertNotEqual(result['guess'], 'a')

    def test_packet_budget_and_empty_dilution(self):
        self.game['facts'] = [
            {'id': 'a-bundle', 'owner': 'a', 'subject': 'a', 'assertions': [
                {'predicate': 'owns_cat', 'value': False, 'source_atom': 'a.no_pets'},
                {'predicate': 'owns_dog', 'value': False, 'source_atom': 'a.no_pets'}]},
            {'id': 'b-flavor', 'owner': 'b', 'subject': 'b', 'assertions': []}]
        self.game['clues'] = [
            {'id': key, 'predicate': key, 'expected': False, 'strength': 'hard',
             'source_atom': key, 'recipients': ['a']} for key in ['owns_cat', 'owns_dog']]
        result = simulate(self.game, partners=3, packets_per_encounter=1)
        for event in result['trace']:
            if event['phase'] == 'mingling':
                self.assertLessEqual(len(event['packets']), 1)
        self.assertTrue(any('fact:b-flavor' in event['packets'] for event in result['trace']))
        candidate = result['full_information']['candidates']['a']
        self.assertEqual(candidate['supported_match_count'], 2)
        self.assertEqual(candidate['unique_source_match_count'], 1)

    def test_group_round_snapshot(self):
        result = simulate(self.game, partners=0, relay=True, group_rounds=1, group_packets=99)
        for event in result['trace']:
            if event['phase'] == 'group':
                sender = event['sender']
                allowed = {'fact:' + f['id'] for f in self.game['facts'] if f['owner'] == sender}
                allowed |= {'clue:' + c['id'] for c in self.game['clues'] if sender in c['recipients']}
                self.assertLessEqual(set(event['packets']), allowed)

    def test_derived_fact_requires_both_received_sources(self):
        self.game['facts'] = [
            {'id':'first','owner':'a','subject':'a','assertions':[{'predicate':'two_jobs','value':True,'source_atom':'first+second','requires':['fact:second']}]},
            {'id':'second','owner':'a','subject':'a','assertions':[]}]
        self.game['clues'] = [{'id':'jobs','predicate':'two_jobs','expected':False,'strength':'hard','source_atom':'jobs','recipients':[]}]
        players,packets=prepare(self.game)
        self.assertIn('a',assess(players,packets,['fact:first','clue:jobs'])['remaining'])
        self.assertNotIn('a',assess(players,packets,['fact:first','fact:second','clue:jobs'])['remaining'])
        self.game['facts'][0]['assertions'][0]['requires']=['fact:missing']
        with self.assertRaises(ValueError):prepare(self.game)


if __name__ == '__main__':
    unittest.main()
