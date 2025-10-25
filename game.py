import pygame
from config import *
from sheep import Sheep
from grass import Collectible, Obstacle, Spawner, Wolf, Projectile
import random
import math
import io
import wave
import struct
import numpy as np
import pygame.sndarray

class Game:
    def __init__(self, screen):
        self.state = 'menu'  # menu, rules, game
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.game_speed = INITIAL_GAME_SPEED

        # groups
        self.sheep_group = pygame.sprite.Group()
        self.collectible_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.wolf_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()

        # create player
        start_x = 100
        start_y = SCREEN_HEIGHT - TILE_SIZE - SHEEP_SIZE
        self.player = Sheep(start_x, start_y)
        self.sheep_group.add(self.player)

        self.spawner = Spawner(self.collectible_group, self.obstacle_group, self.wolf_group)

        # fonts (try to use a pixel-like font if present, otherwise fallback)
        try:
            # try local assets font first
            self.font = pygame.font.Font('assets/fonts/pixel_font.ttf', 20)
        except Exception:
            try:
                self.font = pygame.font.SysFont('Consolas', 20)
            except Exception:
                self.font = pygame.font.Font(None, 20)

        # simple procedural sounds (generate short sine blips)
        try:
            pygame.mixer.init()
        except Exception:
            # mixer may fail in headless/test environments
            pass
        try:
            # allow many overlapping notes
            pygame.mixer.set_num_channels(32)
        except Exception:
            pass
        # eat / grass sound
        self.sound_eat = self._make_sound(660, 0.08)
        # mushroom pickup
        self.sound_mushroom = self._make_sound(330, 0.12)
        # shooting
        self.sound_shoot = self._make_sound(1200, 0.05)
        # jump
        self.sound_jump = self._make_sound(900, 0.05)
        # wolf hit / enemy defeated
        self.sound_wolf = self._make_sound(200, 0.08)
        # game over
        self.sound_over = self._make_sound(150, 0.4)

        # Musical scale mapping (C major by default)
        NOTE_FREQS = {
            'do': 261.63,   # C4
            're': 293.66,   # D4
            'mi': 329.63,   # E4
            'fa': 349.23,   # F4
            'so': 392.00,   # G4
            'la': 440.00,   # A4
            'ti': 493.88,   # B4
        }

        # map collectible kinds/colors to note names (green=do, pink=re(rai), blue=mi, plus 4 more)
        self.kind_to_note = {
            'grass': 'do',
            'mushroom_pink': 're',
            'mushroom_blue': 'mi',
            'mushroom_yellow': 'fa',
            'mushroom_orange': 'so',
            'mushroom_purple': 'la',
            'mushroom_cyan': 'ti',
        }

        # pre-generate sounds for each note so collecting feels instantaneous
        self.note_sounds = {}
        for k, note in self.kind_to_note.items():
            freq = NOTE_FREQS.get(note, 440.0)
            # generate a longer, musically-shaped note (ADSR envelope)
            self.note_sounds[k] = self._make_note_sound(freq, duration=0.35, volume=0.35)

        # background music (simple loop) - use already-imported numpy and pygame.sndarray
        try:
            samplerate = 22050
            duration = 2.0
            t = np.linspace(0, duration, int(samplerate * duration), False)
            melody = np.sin(2 * np.pi * t * 220) * 0.2
            melody += np.sin(2 * np.pi * t * 440) * 0.1
            melody += np.sin(2 * np.pi * t * 660) * 0.05
            arr = np.array(melody * 32767, dtype=np.int16)
            arr = arr.reshape(-1, 1)
            sound = pygame.sndarray.make_sound(arr)
            sound.play(-1)
        except Exception:
            pass

        self.score = 0
        # effect timers
        self.effect = None
        self.effect_timer = 0
        self.effect_bg = None

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == 'menu':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    # Start button
                    if 300 < mx < 500 and 250 < my < 310:
                        self.state = 'game'
                    # Rules button
                    if 300 < mx < 500 and 320 < my < 380:
                        self.state = 'rules'
            elif self.state == 'rules':
                if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    self.state = 'menu'
            elif self.state == 'game':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                    self.reset()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    px = self.player.rect.right
                    py = self.player.rect.centery
                    self.projectile_group.add(Projectile(px, py))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    px = self.player.rect.right
                    py = self.player.rect.centery
                    self.projectile_group.add(Projectile(px, py))

    def reset(self):
        self.game_over = False
        self.score = 0
        self.game_speed = INITIAL_GAME_SPEED
        self.collectible_group.empty()
        self.obstacle_group.empty()
        self.player.rect.topleft = (100, SCREEN_HEIGHT - TILE_SIZE - SHEEP_SIZE)
        self.player.vx = 0
        self.player.vy = 0
        self.player.size_mod = 1.0
        self.effect = None
        self.effect_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.game_over:
            # effect timer
            if self.effect_timer > 0:
                self.effect_timer -= 1
                if self.effect_timer == 0:
                    self._clear_effect()

            self.player.update(keys, self.game_speed)
            # play jump sound if the sheep initiated a jump this frame
            try:
                if getattr(self.player, 'last_jumped', False):
                    self.sound_jump.play()
            except Exception:
                pass
            # spawn
            self.spawner.maybe_spawn(self.game_speed)
            # update groups
            self.collectible_group.update(self.game_speed)
            self.obstacle_group.update(self.game_speed)
            self.wolf_group.update(self.game_speed)
            self.projectile_group.update(self.game_speed)

            # collisions with collectibles
            hits = pygame.sprite.spritecollide(self.player, self.collectible_group, dokill=True)
            for c in hits:
                # double score for pink/blue mushrooms
                if c.kind in ('mushroom_pink', 'mushroom_blue'):
                    self.score += c.value * 2
                else:
                    self.score += c.value
                # play musical note mapped to this collectible kind
                try:
                    snd = self.note_sounds.get(c.kind, None)
                    if snd:
                        snd.play()
                    else:
                        # fallback eat sound
                        self.sound_eat.play()
                except Exception:
                    pass
                # handle colored mushroom effects
                if c.kind.startswith('mushroom'):
                    self.effect = c.kind
                    self.effect_timer = FPS * 3
                    self.effect_bg = Collectible.BG_MAP.get(c.kind, None)
            # projectile-wolf collision
            for wolf in pygame.sprite.groupcollide(self.wolf_group, self.projectile_group, True, True):
                try:
                    self.sound_wolf.play()
                except Exception:
                    pass
                # reward points for defeating a wolf
                self.score += 5
            # collisions with obstacles
            if pygame.sprite.spritecollideany(self.player, self.obstacle_group):
                self.game_over = True
                try:
                    self.sound_over.play()
                except Exception:
                    pass
            # wolf-player collision (game over)
            if pygame.sprite.spritecollideany(self.player, self.wolf_group):
                self.game_over = True

            # increase speed
            self.game_speed += SPEED_INCREMENT

    def _clear_effect(self):
        self.effect = None
        self.effect_bg = None

    def draw_background(self):
        # colored theme if mushroom effect
        if self.effect_bg:
            bg1 = self.effect_bg
            bg2 = tuple(min(255, int(c*0.9)) for c in self.effect_bg)
        else:
            bg1 = BG_COLOR
            bg2 = BG_COLOR_ALT
        tile_h = TILE_SIZE
        for y in range(0, SCREEN_HEIGHT, tile_h):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                color = bg1 if ((x//TILE_SIZE + y//TILE_SIZE) % 2 == 0) else bg2
                pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        # ground line
        pygame.draw.rect(self.screen, (50,160,40), (0, SCREEN_HEIGHT - TILE_SIZE, SCREEN_WIDTH, TILE_SIZE))

    def render(self):
        self.draw_background()
        # draw sprites
        self.collectible_group.draw(self.screen)
        self.obstacle_group.draw(self.screen)
        self.wolf_group.draw(self.screen)
        self.projectile_group.draw(self.screen)
        self.sheep_group.draw(self.screen)

        # UI
        score_surf = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_surf, (10,10))

        if self.game_over:
            over_surf = self.font.render("Game Over - Press R to Restart", True, (200,0,0))
            rect = over_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(over_surf, rect)

        pygame.display.flip()

    def run_frame(self):
        self.process_events()
        if self.state == 'menu':
            self.render_menu()
        elif self.state == 'rules':
            self.render_rules()
        elif self.state == 'game':
            self.update()
            self.render()
        self.clock.tick(FPS)
    def render_menu(self):
        self.screen.fill((255, 220, 250))
        title = self.font.render("Sheep Runner!", True, (255, 100, 180))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
        # Cute sheep face
        pygame.draw.ellipse(self.screen, (255,255,255), (360,170,80,50))
        pygame.draw.circle(self.screen, (255,200,200), (400,195), 20)
        pygame.draw.circle(self.screen, (0,0,0), (390,195), 5)
        pygame.draw.circle(self.screen, (0,0,0), (410,195), 5)
        # Start button
        pygame.draw.rect(self.screen, (255,240,200), (300,250,200,60), border_radius=20)
        start_txt = self.font.render("Start Game", True, (120,60,200))
        self.screen.blit(start_txt, (SCREEN_WIDTH//2 - start_txt.get_width()//2, 265))
        # Rules button
        pygame.draw.rect(self.screen, (220,240,255), (300,320,200,60), border_radius=20)
        rules_txt = self.font.render("Game Rules", True, (60,120,200))
        self.screen.blit(rules_txt, (SCREEN_WIDTH//2 - rules_txt.get_width()//2, 335))
        # Footer
        footer = self.font.render("Click to select", True, (120,120,120))
        self.screen.blit(footer, (SCREEN_WIDTH//2 - footer.get_width()//2, 400))
        pygame.display.flip()

    def render_rules(self):
        self.screen.fill((240,240,255))
        title = self.font.render("Game Rules", True, (100,100,255))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        lines = [
            "Control the sheep with A/D or arrow keys.",
            "Jump with Space, W, or Up (double jump possible).",
            "Eat grass and mushrooms for points and effects.",
            "Avoid obstacles and wolves!",
            "Shoot wolves with Space or Left Mouse.",
            "Game ends if you hit an obstacle or wolf.",
            "Click or press any key to return."
        ]
        for i, line in enumerate(lines):
            txt = self.font.render(line, True, (80,80,120))
            self.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, 140 + i*40))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.run_frame()
        pygame.quit()

    def _make_sound(self, freq, duration, volume=0.2, samplerate=44100):
        """Generate a short sine wave sound and return a pygame Sound object."""
        n_samples = int(samplerate * duration)
        buf = bytearray()
        for i in range(n_samples):
            t = i / samplerate
            # simple envelope
            env = 1.0
            val = int(volume * 32767 * math.sin(2 * math.pi * freq * t) * env)
            buf += struct.pack('<h', val)
        # create pygame Sound from bytes
        try:
            sound = pygame.mixer.Sound(buffer=bytes(buf))
            return sound
        except Exception:
            # fallback: silent sound
            arr = pygame.sndarray.make_sound(pygame.surfarray.array2d(pygame.Surface((1,1))))
            return arr

    def _make_note_sound(self, freq, duration=0.35, volume=0.4, samplerate=44100):
        """Generate a musical note with a simple ADSR envelope and return a pygame Sound.

        Uses numpy for efficient waveform and envelope generation.
        """
        try:
            n = int(samplerate * duration)
            t = np.linspace(0, duration, n, False)
            # sine waveform
            wave_data = np.sin(2 * np.pi * freq * t)
            # simple ADSR envelope
            attack = int(0.02 * samplerate)
            decay = int(0.05 * samplerate)
            release = int(0.12 * samplerate)
            sustain_len = max(0, n - (attack + decay + release))
            # build envelope
            env = np.concatenate([
                np.linspace(0.0, 1.0, attack, False) if attack > 0 else np.array([]),
                np.linspace(1.0, 0.7, decay, False) if decay > 0 else np.array([]),
                np.ones(sustain_len) * 0.7 if sustain_len > 0 else np.array([]),
                np.linspace(0.7, 0.0, release, False) if release > 0 else np.array([]),
            ])
            if env.size < wave_data.size:
                # pad envelope if rounding made it shorter
                env = np.pad(env, (0, wave_data.size - env.size), mode='constant', constant_values=(0,))
            env = env[:wave_data.size]
            samples = (wave_data * env * (volume * 32767)).astype(np.int16)
            # mono -> stereo column for pygame
            arr = samples.reshape(-1, 1)
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except Exception:
            # fallback to short beep
            return self._make_sound(freq, min(duration, 0.12), volume=volume)
