import pygame

class Wolf(pygame.sprite.Sprite):
    """Enemy wolf that moves left."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill((128,128,128))
        pygame.draw.rect(self.image, (80,80,80), (8,8,16,16))
        pygame.draw.rect(self.image, (255,255,255), (20,12,8,8)) # eye
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vx = -4
    def update(self, game_speed):
        self.rect.x += int(self.vx * game_speed)
        if self.rect.right < 0:
            self.kill()

class Projectile(pygame.sprite.Sprite):
    """Projectile fired by sheep."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12,6))
        self.image.fill((255,220,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = 10
    def update(self, game_speed):
        self.rect.x += int(self.vx * game_speed)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
import pygame
import pygame
import random
from config import *


class Collectible(pygame.sprite.Sprite):
    """Base class for all collectibles (grass, colored mushrooms)."""
    COLOR_MAP = {
        'grass': (34,139,34),
        'mushroom_pink': (255,192,203),
        'mushroom_blue': (135,206,250),
        'mushroom_yellow': (255,255,102),
        'mushroom_orange': (255,165,0),
        'mushroom_purple': (200,162,200),
        'mushroom_cyan': (102,255,255),
    }
    BG_MAP = {
        'mushroom_pink': (255,192,203),
        'mushroom_blue': (135,206,250),
        'mushroom_yellow': (255,255,102),
        'mushroom_orange': (255,165,0),
        'mushroom_purple': (200,162,200),
        'mushroom_cyan': (102,255,255),
    }
    def __init__(self, x, y, kind='grass', value=SCORE_PER_GRASS):
        super().__init__()
        self.kind = kind
        self.value = value
        self.image = pygame.Surface((GRASS_SIZE, GRASS_SIZE))
        color = self.COLOR_MAP.get(kind, (255,255,255))
        self.image.fill(color)
        if kind.startswith('mushroom'):
            pygame.draw.ellipse(self.image, color, (0,0,GRASS_SIZE,GRASS_SIZE//2))
            pygame.draw.rect(self.image, (255,255,255), (GRASS_SIZE//3,GRASS_SIZE//2,GRASS_SIZE//3,GRASS_SIZE//2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, game_speed):
        self.rect.x -= int(game_speed * 2)
        if self.rect.right < 0:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    """Simple obstacle like stone or stump."""
    def __init__(self, x, y, w=OBSTACLE_SIZE, h=OBSTACLE_SIZE):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((100,100,100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, game_speed):
        self.rect.x -= int(game_speed * 2)
        if self.rect.right < 0:
            self.kill()


class Spawner:
    def __init__(self, collectible_group, obstacle_group, wolf_group):
        self.collectible_group = collectible_group
        self.obstacle_group = obstacle_group
        self.wolf_group = wolf_group

    def maybe_spawn(self, game_speed):
        # spawn collectibles
        if random.random() < GRASS_SPAWN_RATE:
            x = SCREEN_WIDTH + 10
            y = SCREEN_HEIGHT - TILE_SIZE - GRASS_SIZE
            # Increase frequency of colorful mushrooms so player plays more notes
            kind = random.choices(
                ['grass', 'mushroom_pink', 'mushroom_blue', 'mushroom_yellow', 'mushroom_orange', 'mushroom_purple', 'mushroom_cyan'],
                # weights sum to 1.0; more chance for colored mushrooms
                weights=[0.50, 0.12, 0.12, 0.06, 0.06, 0.07, 0.07]
            )[0]
            c = Collectible(x, y, kind=kind)
            self.collectible_group.add(c)
        # spawn obstacle (further reduced rate)
        if random.random() < (OBSTACLE_SPAWN_RATE * 0.25):
            x = SCREEN_WIDTH + 20
            y = SCREEN_HEIGHT - TILE_SIZE - OBSTACLE_SIZE
            o = Obstacle(x, y)
            self.obstacle_group.add(o)
        # spawn wolf (reduced rate)
        if random.random() < 0.003:
            x = SCREEN_WIDTH + 40
            y = SCREEN_HEIGHT - TILE_SIZE - OBSTACLE_SIZE
            w = Wolf(x, y)
            self.wolf_group.add(w)
