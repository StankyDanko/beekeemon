# screens/main_menu.py
# Heartbeat Satellite: Beekeemon’s entry UI—starts the buzz and loads saves!
# Integration: Links to utils/save_load.py for loading, switches to world_map.py via main.py.
# Repo: https://github.com/StankyDanko/beekeemon/tree/main/screens

import pygame
import random
from utils.save_load import load_game
from classes.Bee import Bee
from classes.Hive import Hive

class MainMenuScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.options = ["New Game", "Load Slot 1", "Load Slot 2", "Load Slot 3"]
        self.selected = 0
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 255, 0)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    self.start_new_game()
                elif self.selected in [1, 2, 3]:
                    slot = self.selected
                    data = load_game(slot)
                    if data:
                        self.game.current_slot = slot
                        self.game.screens["world_map"].load_data(data)
                        self.game.switch_screen("world_map")

    def update(self):
        pass

    def render(self):
        self.game.screen.fill(self.bg_color)
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected else self.text_color
            text = self.font.render(option, True, color)
            self.game.screen.blit(text, (300, 200 + i * 50))

    def start_new_game(self):
        self.game.current_slot = None
        self.game.screens["world_map"].player.x = 400
        self.game.screens["world_map"].player.y = 300
        self.game.bees = [Bee("Queen"), Bee("Drone"), Bee("Drone"), Bee("Worker"), Bee("Worker")]
        self.game.hive = Hive(self.game.bees[0])
        self.game.switch_screen("world_map")