# classes/Bee.py
# Heartbeat Satellite: The hive’s lifeblood—bees with personality and purpose!
# Integration: Spawned by main.py, moves in world_map.py, stats in bee_inspector.py,
# impacts Hive (classes/Hive.py). Repo: https://github.com/StankyDanko/beekeemon/tree/main/classes

import random
import pygame
import logging
from classes.Personality import PERSONALITY_TYPES

class Bee:
    def __init__(self, type, personality=None):
        self.type = type
        logging.info(f"Creating bee of type: {self.type}")
        self.personality = personality if personality else random.choice([p[0] for p in PERSONALITY_TYPES])
        self.gender = self._set_gender()
        self.attributes = self._set_attributes()
        self.health = 100
        self.energy = 100
        self.x = 400 + random.randint(-50, 50)
        self.y = 300 + random.randint(-50, 50)
        self.speed = 2
        self.image = self._set_image()

    def _set_gender(self):
        if self.type == "Queen":
            return "Female"
        elif self.type == "Drone":
            return "Male"
        elif self.type == "Worker":
            return random.choice(["Male", "Female"])
        return None

    def _set_attributes(self):
        personality_info = next(ptype for ptype in PERSONALITY_TYPES if ptype[0] == self.personality)
        base_ranges = personality_info[1]
        attributes = {}
        modifiers = {
            "Queen": {"Foraging": 0.5, "Resilience": 1.2, "Communication": 1.5},
            "Drone": {"Foraging": 0.2, "Resilience": 0.8, "Communication": 1.0},
            "Worker": {"Foraging": 1.0, "Resilience": 1.0, "Communication": 1.0}
        }
        type_mod = modifiers.get(self.type, {"Foraging": 1.0, "Resilience": 1.0, "Communication": 1.0})
        for attr, (min_val, max_val) in base_ranges.items():
            adjusted_min = min_val * type_mod[attr]
            adjusted_max = max_val * type_mod[attr]
            attributes[attr] = random.uniform(adjusted_min, adjusted_max)
        return attributes

    def _set_image(self):
        try:
            if self.type == "Queen":
                image = pygame.image.load("assets/bee_queen.png").convert_alpha()
            elif self.type == "Drone":
                image = pygame.image.load("assets/bee_drone.png").convert_alpha()
            elif self.type == "Worker":
                image = pygame.image.load("assets/bee_worker.png").convert_alpha()
            else:
                image = pygame.image.load("assets/bee_worker.png").convert_alpha()
            logging.info(f"Successfully loaded image for {self.type}")
            return image
        except pygame.error as e:
            logging.error(f"Error loading image for {self.type}: {e}")
            default_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
            default_surface.fill((255, 0, 0))
            return default_surface

    def attempt_mating(self, queen):
        if self.type != "Drone":
            return False
        compatibility = self.attributes["Resilience"] - (queen.attributes["Resilience"] - 0.3)
        success = random.random() < compatibility
        return success if compatibility > 0 else False

    def get_task_efficiency(self):
        if self.type != "Worker":
            return 0
        return self.attributes["Foraging"] * 0.1

    def render(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))