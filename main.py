# main.py
# Heartbeat Satellite: Launches Beekeemon, uniting hive and screens—our buzzing core!
# Integration: Initializes Bees (classes/Bee.py), Hive (classes/Hive.py), and Player (classes/Player.py),
# passing them to screens/world_map.py for gameplay. See repo: https://github.com/StankyDanko/beekeemon

import pygame
import random
import logging
from screens.main_menu import MainMenuScreen
from screens.world_map import WorldMapScreen
from classes.Bee import Bee
from classes.Hive import Hive

# Logging setup—tracks hive pulse in beekeemon.log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('beekeemon.log', mode='w'), logging.StreamHandler()]
)

class Game:
    def __init__(self):
        try:
            logging.info("Initializing Pygame")
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Beekeemon")
            self.clock = pygame.time.Clock()
            self.current_slot = None
            logging.info("Creating initial bees")
            self.bees = [Bee("Queen"), Bee("Drone"), Bee("Drone"), Bee("Worker"), Bee("Worker")]
            self.hive = Hive(self.bees[0])
            logging.info("Initializing screens")
            self.screens = {
                "main_menu": MainMenuScreen(self),
                "world_map": WorldMapScreen(self),
                "bee_inspector": None
            }
            self.current_screen = self.screens["main_menu"]
            logging.info("Game initialization complete")
        except Exception as e:
            logging.error(f"Error in Game.__init__: {e}", exc_info=True)
            raise

    def switch_screen(self, screen_name):
        try:
            logging.info(f"Switching to screen: {screen_name}")
            self.current_screen = self.screens[screen_name]
        except Exception as e:
            logging.error(f"Error in switch_screen: {e}", exc_info=True)
            raise

    def run(self):
        try:
            logging.info("Starting game loop")
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        logging.info("Quit event received")
                        pygame.quit()
                        return
                    self.current_screen.handle_event(event)
                self.current_screen.update()
                self.current_screen.render()
                pygame.display.flip()
                self.clock.tick(60)
        except Exception as e:
            logging.error(f"Error in game loop: {e}", exc_info=True)
            pygame.quit()
            raise

if __name__ == "__main__":
    try:
        logging.info("Launching Beekeemon")
        game = Game()
        game.run()
    except Exception as e:
        logging.error(f"Error in main: {e}", exc_info=True)
        pygame.quit()