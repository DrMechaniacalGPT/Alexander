"""Finite pair schedules with guaranteed distinct partners; no game-content input."""
import random


def distinct_encounters(players, partners, seed=1, turns_each=2, instruction='Talk about what matters to you.'):
    players = list(players)
    if len(players) < 2 or len(players) % 2 or len(set(players)) != len(players):
        raise ValueError('Distinct-partner schedule requires an even number of unique players')
    if not isinstance(partners, int) or not 1 <= partners < len(players):
        raise ValueError('Partner count must be between one and player count minus one')
    if not isinstance(turns_each, int) or not 1 <= turns_each <= 20:
        raise ValueError('Invalid turn budget')
    ring = players[:]
    random.Random(seed).shuffle(ring)
    result = []
    for window in range(partners):
        for i in range(len(ring)//2):
            result.append({'participants': [ring[i], ring[-i-1]], 'turns_each': turns_each,
                           'instruction': instruction, 'window': window})
        ring = [ring[0], ring[-1], *ring[1:-1]]
    return result
