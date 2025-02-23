# classes/Player.py
# Heartbeat Satellite: The beekeeper’s soul—moves and leads the hive!
# Integration: Controlled by world_map.py, renders via main.py’s screen setup.
# Repo: https://github.com/StankyDanko/beekeemon/tree/main/classes

import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.image.load("assets/player.png").convert_alpha()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def render(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))