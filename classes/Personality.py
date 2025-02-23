# classes/Personality.py
# Heartbeat Satellite: Bees’ quirky souls—defines personality traits!
# Integration: Used by Bee.py (classes/Bee.py) to tweak attributes.
# Repo: https://github.com/StankyDanko/beekeemon/tree/main/classes

PERSONALITY_TYPES = [
    ("Forager", {'Foraging': (0.7, 1.0), 'Resilience': (0.4, 0.7), 'Communication': (0.5, 0.8)}),
    ("Guardian", {'Foraging': (0.3, 0.6), 'Resilience': (0.7, 1.0), 'Communication': (0.4, 0.7)}),
    ("Communicator", {'Foraging': (0.4, 0.7), 'Resilience': (0.5, 0.8), 'Communication': (0.7, 1.0)}),
]