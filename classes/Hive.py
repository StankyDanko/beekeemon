# classes/Hive.py
# Heartbeat Satellite: The hive’s humming center—tracks growth and honey!
# Integration: Updated by world_map.py with Bee (classes/Bee.py) actions, stats shown on-screen.
# Repo: https://github.com/StankyDanko/beekeemon/tree/main/classes

import logging

class Hive:
    def __init__(self, queen):
        self.queen = queen
        self.growth_rate = self._calculate_growth_rate()
        self.honey = 0
        self.population = 5

    def _calculate_growth_rate(self):
        base_rate = 0.1
        queen_bonus = self.queen.attributes["Communication"] * 0.2
        return base_rate + queen_bonus

    def update(self, mating_success=False, worker_efficiency=0):
        try:
            growth = self.growth_rate
            if mating_success:
                growth += 0.1
            self.population += growth
            self.honey += worker_efficiency
            logging.info(f"Hive updated: Population={self.population:.2f}, Honey={self.honey:.2f}")
        except Exception as e:
            logging.error(f"Error in Hive.update: {e}", exc_info=True)
            raise