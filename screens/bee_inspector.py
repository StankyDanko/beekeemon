# screens/bee_inspector.py
# Heartbeat Satellite: Peek into the hive—shows bee stats with flair!
# Integration: Displays Bee (classes/Bee.py) data from world_map.py clicks, returns via ESC key.
# Repo: https://github.com/StankyDanko/beekeemon/tree/main/screens

import pygame

class BeeInspectorScreen:
    def __init__(self, game, bee):
        self.game = game
        self.bee = bee
        self.font = pygame.font.Font(None, 24)
        self.bg_color = (0, 0, 0)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.switch_screen("world_map")

    def update(self):
        pass

    def render(self):
        self.game.screen.fill(self.bg_color)
        lines = [
            f"Type: {self.bee.type}",
            f"Gender: {self.bee.gender}",
            f"Personality: {self.bee.personality}"
        ]
        y = 50
        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            self.game.screen.blit(text, (50, y))
            y += 30
        for attr, value in self.bee.attributes.items():
            text = self.font.render(f"{attr}: {value:.2f}", True, (255, 255, 255))
            self.game.screen.blit(text, (50, y))
            y += 30