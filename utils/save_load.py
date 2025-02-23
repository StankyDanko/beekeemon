# utils/save_load.py
# Heartbeat Satellite: Keeps the hive’s memory—saves and loads state!
# Integration: Used by main_menu.py and world_map.py for persistence.
# Repo: https://github.com/StankyDanko/beekeemon/tree/main/utils

import json
import os
import logging

def save_game(slot, player, bees):
    try:
        data = {
            "player": {"x": player.x, "y": player.y},
            "bees": [{"x": bee.x, "y": bee.y} for bee in bees]
        }
        if not os.path.exists("saves"):
            os.makedirs("saves")
        with open(f"saves/slot_{slot}.json", "w") as f:
            json.dump(data, f)
        logging.info(f"Game saved to slot_{slot}.json")
    except Exception as e:
        logging.error(f"Error saving game to slot {slot}: {e}", exc_info=True)
        raise

def load_game(slot):
    try:
        with open(f"saves/slot_{slot}.json", "r") as f:
            data = json.load(f)
            logging.info(f"Loaded game from slot_{slot}.json")
            return data
    except FileNotFoundError:
        logging.info(f"No save found in Slot {slot}")
        return None
    except Exception as e:
        logging.error(f"Error loading game from slot {slot}: {e}", exc_info=True)
        raise