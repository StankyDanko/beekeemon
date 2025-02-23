# screens/world_map.py
# Heartbeat Satellite: Beekeemon’s buzzing world—where bees follow and hives thrive!
# Integration: Drives Player (classes/Player.py), Bee (classes/Bee.py), and Hive (classes/Hive.py)
# updates; uses utils/save_load.py for persistence. Repo: https://github.com/StankyDanko/beekeemon/tree/main/screens

import pygame
import random
import logging
from classes.Player import Player
from utils.save_load import save_game
from screens.bee_inspector import BeeInspectorScreen

class WorldMapScreen:
    def __init__(self, game):
        try:
            self.game = game
            logging.info("Creating player at (400, 300)")
            self.player = Player(400, 300)
            self.font = pygame.font.Font(None, 20)
            self.save_slot_active = False
            self.save_slot_options = ["Slot 1", "Slot 2", "Slot 3"]
            self.save_slot_selected = 0
            self.menu_font = pygame.font.Font(None, 36)
            self.menu_bg = pygame.Surface((300, 200), pygame.SRCALPHA)
            self.menu_bg.fill((0, 0, 0, 180))
            logging.info("WorldMapScreen initialized")
        except Exception as e:
            logging.error(f"Error in WorldMapScreen.__init__: {e}", exc_info=True)
            raise

    def load_data(self, data):
        try:
            logging.info("Loading save data into WorldMapScreen")
            self.player.x = data["player"]["x"]
            self.player.y = data["player"]["y"]
            for i, bee_data in enumerate(data["bees"]):
                if i < len(self.game.bees):
                    self.game.bees[i].x = bee_data["x"]
                    self.game.bees[i].y = bee_data["y"]
            logging.info("Save data loaded successfully")
        except Exception as e:
            logging.error(f"Error in load_data: {e}", exc_info=True)
            raise

    def handle_event(self, event):
        try:
            if event.type == pygame.KEYDOWN:
                if self.save_slot_active:
                    if event.key == pygame.K_UP:
                        self.save_slot_selected = (self.save_slot_selected - 1) % len(self.save_slot_options)
                    elif event.key == pygame.K_DOWN:
                        self.save_slot_selected = (self.save_slot_selected + 1) % len(self.save_slot_options)
                    elif event.key == pygame.K_RETURN:
                        slot = self.save_slot_selected + 1
                        logging.info(f"Saving game to slot {slot}")
                        save_game(slot, self.player, self.game.bees)
                        self.game.current_slot = slot
                        self.save_slot_active = False
                    elif event.key == pygame.K_ESCAPE:
                        self.save_slot_active = False
                else:
                    if event.key == pygame.K_m:
                        self.game.switch_screen("main_menu")
                    elif event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                        logging.info("Ctrl+S pressed, opening save slot menu")
                        self.save_slot_active = True
                        self.save_slot_selected = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for bee in self.game.bees:
                    if (bee.x - pos[0])**2 + (bee.y - pos[1])**2 < 100:
                        logging.info(f"Bee clicked at ({bee.x}, {bee.y}), switching to inspector")
                        self.game.screens["bee_inspector"] = BeeInspectorScreen(self.game, bee)
                        self.game.switch_screen("bee_inspector")
                        break
        except Exception as e:
            logging.error(f"Error in handle_event: {e}", exc_info=True)
            raise

    def update(self):
        try:
            if not self.save_slot_active:
                self.player.update()
                queen = next((bee for bee in self.game.bees if bee.type == "Queen"), None)
                if queen:
                    for bee in self.game.bees:
                        dx = self.player.x - bee.x
                        dy = self.player.y - bee.y
                        distance = (dx**2 + dy**2)**0.5
                        if distance > 10:
                            bee.x += (dx / distance) * bee.speed
                            bee.y += (dy / distance) * bee.speed
                    mating_success = False
                    for drone in [b for b in self.game.bees if b.type == "Drone"]:
                        if random.random() < 0.01:
                            if drone.attempt_mating(queen):
                                logging.info(f"Drone at ({drone.x}, {drone.y}) successfully mated with Queen")
                                mating_success = True
                    workers = [b for b in self.game.bees if b.type == "Worker"]
                    worker_efficiency = 0
                    if len(workers) >= 2:
                        w1, w2 = workers[:2]
                        base_eff = w1.get_task_efficiency() + w2.get_task_efficiency()
                        compatibility = 1.2 if w1.personality == w2.personality else 0.8
                        worker_efficiency = base_eff * compatibility
                        logging.info(f"Worker efficiency: {worker_efficiency:.2f}, Compatibility: {compatibility}")
                    self.game.hive.update(mating_success, worker_efficiency)
        except Exception as e:
            logging.error(f"Error in update: {e}", exc_info=True)
            raise

    def render(self):
        try:
            self.game.screen.fill((0, 100, 0))
            self.player.render(self.game.screen)
            for bee in self.game.bees:
                bee.render(self.game.screen)
            hive_stats = [
                f"Pop: {self.game.hive.population:.1f}",
                f"Honey: {self.game.hive.honey:.1f}"
            ]
            for i, stat in enumerate(hive_stats):
                text = self.font.render(stat, True, (255, 255, 255))
                self.game.screen.blit(text, (10, 10 + i * 20))
            if self.save_slot_active:
                menu_x = (800 - 300) // 2
                menu_y = (600 - 200) // 2
                self.game.screen.blit(self.menu_bg, (menu_x, menu_y))
                for i, option in enumerate(self.save_slot_options):
                    color = (255, 255, 0) if i == self.save_slot_selected else (255, 255, 255)
                    text = self.menu_font.render(option, True, color)
                    text_x = menu_x + (300 - text.get_width()) // 2
                    text_y = menu_y + 50 + i * 50
                    self.game.screen.blit(text, (text_x, text_y))
        except Exception as e:
            logging.error(f"Error in render: {e}", exc_info=True)
            raise