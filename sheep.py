import pygame
import math
from config import *

class Sheep(pygame.sprite.Sprite):
    """Player sheep sprite. Simple rectangle/pixel placeholder animations."""
    def __init__(self, x, y):
        super().__init__()
        self.width = SHEEP_SIZE
        self.height = SHEEP_SIZE
        self.prev_jump_pressed = False
        # Simple surface as placeholder pixel art (two-frame animation)
        self.frames = [pygame.Surface((self.width, self.height)), pygame.Surface((self.width, self.height))]
        # draw simple sheep pixels
        for i, surf in enumerate(self.frames):
            surf.fill((0,0,0))
            surf.set_colorkey((0,0,0))
            # body
            pygame.draw.rect(surf, (240,240,240), (4,8,24,16))
            # head
            pygame.draw.rect(surf, (220,220,220), (0,8,8,8))
            # eye
            pygame.draw.rect(surf, (0,0,0), (2,10,2,2))
            # leg animation
            if i == 0:
                pygame.draw.rect(surf, (120,120,120), (8,24,4,8))
                pygame.draw.rect(surf, (120,120,120), (20,24,4,8))
            else:
                pygame.draw.rect(surf, (120,120,120), (12,24,4,8))
                pygame.draw.rect(surf, (120,120,120), (16,24,4,8))
        self.anim_index = 0
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # physics
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.jump_count = 0
        self.size_mod = 1.0
        self.flying = False
        self.prev_jump_pressed = False

    def update(self, keys, game_speed):
        # apply size_mod (grow effect)
        if self.size_mod != 1.0:
            w = int(self.width * self.size_mod)
            h = int(self.height * self.size_mod)
            self.image = pygame.transform.scale(self.frames[self.anim_index], (w, h))
            self.rect = self.image.get_rect(center=self.rect.center)
        # horizontal movement
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -SHEEP_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = SHEEP_SPEED
        # update horizontal position and clamp inside screen
        new_x = int(self.rect.x + (self.vx * game_speed))
        # clamp to screen bounds
        new_x = max(0, min(new_x, SCREEN_WIDTH - self.width))
        self.rect.x = new_x

        # clamp to screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # jump (W/up) - allow multi-jump, debounce
        jump_pressed = keys[pygame.K_w] or keys[pygame.K_UP]
        if jump_pressed and not self.prev_jump_pressed and self.jump_count < MAX_JUMPS:
            self.vy = SHEEP_JUMP_SPEED
            self.on_ground = False
            self.jump_count += 1
        self.prev_jump_pressed = jump_pressed

        # gravity
        if not self.flying:
            self.vy += GRAVITY
        else:
            # balloon effect: float up and down
            self.vy = math.sin(pygame.time.get_ticks() / 200) * 2
        self.rect.y += int(self.vy)

        # ground clamp
        ground_y = SCREEN_HEIGHT - TILE_SIZE - self.rect.height
        if self.rect.y >= ground_y:
            self.rect.y = ground_y
            self.vy = 0
            self.on_ground = True
            self.jump_count = 0

        # animate
        self.anim_index = (self.anim_index + 1) % len(self.frames)
        self.image = self.frames[self.anim_index]

    def eat(self):
        # could play animation/sound
        pass
