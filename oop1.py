# ALL THE THING THAT IS IN THE GAME ARE AN CLASS
# THE DATA OR VARIABLE OF THE GAME ELEMENT ARE MEMBER DATA

# ALL THE IMPORTS
import pygame
import random
import math
import time
from pygame import mixer

# PYGAME INIT
pygame.init()
clock = pygame.time.Clock()

# GLOBLE VARIABLE
scoree = 0

# CONSTENTS
PLAYER_Y = 700
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
PLAYER_SPEED = 0.3
IMAGE_X = 50
IMAGE_Y = IMAGE_X
NUMBER_OF_ENEMY = 5
BULLET_SPEED = PLAYER_SPEED + 0.2

# SCREEN AND GLOBEL DEFINATION
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pew pew with oop")
ICON = pygame.image.load("ufo.png")
pygame.display.set_icon(ICON)

ENEMYIMAGE = pygame.image.load("enemy.png")
ENEMYIMAGE = pygame.transform.smoothscale(ENEMYIMAGE, (IMAGE_X, IMAGE_Y))

PLAYERIMAGE = pygame.image.load("spaceship.png")
PLAYERIMAGE = pygame.transform.smoothscale(PLAYERIMAGE, (IMAGE_X, IMAGE_Y))

BULLETIMAGE = pygame.image.load("m.png")
BULLETIMAGE = pygame.transform.smoothscale(BULLETIMAGE, (IMAGE_X - 25, IMAGE_Y - 25))

BACKGROUND = pygame.image.load("b.jpg")
BACKGROUND = pygame.transform.smoothscale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

# FONT / SCORE
SMALL_FONT = pygame.font.Font("freesansbold.ttf", 20)
BIG_FONT = pygame.font.Font("freesansbold.ttf", 50)



class player:
    def __init__(self, player_x, player_speed, image):
        self.player_x = player_x
        self.player_speed = player_speed
        self.image = image

    def move(self, dt):
        self.player_x += self.player_speed * dt * 1000
        if self.player_x > SCREEN_WIDTH - 50:
            self.player_x = SCREEN_WIDTH - 50
        if self.player_x < 0:
            self.player_x = 0

    def draw(self):
        screen.blit(self.image, (self.player_x, PLAYER_Y))


class ENEMY:
    def __init__(self):
        self.enemy_image = ENEMYIMAGE
        self.enemy_x = random.randint(50, SCREEN_WIDTH - 50)
        self.enemy_y = 50
        self.enemy_speed_x = 0.1
        self.enemy_speed_y = -0.01

    def move(self, dt):
        if self.enemy_x <= 0 or self.enemy_x >= 550:
            self.enemy_speed_x = -self.enemy_speed_x
        self.enemy_x += self.enemy_speed_x * dt * 1000
        self.enemy_y -= self.enemy_speed_y * dt * 1000

    def draw(self):
        screen.blit(self.enemy_image, (self.enemy_x, self.enemy_y))

    def respawn(self):
        self.enemy_y = 50
        self.enemy_x = random.randint(50, SCREEN_WIDTH - 50)
        self.enemy_speed_y -= 0.003

    def did_enemy_reached_player(self):
        return self.enemy_y >= 675


class BULLET:
    def __init__(self, bullet_speed):
        self.bullet_x = -20
        self.bullet_y = PLAYER_Y
        self.bullet_speed = bullet_speed
        self.bullet_image = BULLETIMAGE
        self.bullet_state = "ready"

    def draw(self):
        screen.blit(self.bullet_image, (self.bullet_x, self.bullet_y))

    def fire(self, player_x, player_y):
        if self.bullet_state == "ready":
            self.bullet_x = player_x + 10
            self.bullet_y = player_y
            self.bullet_state = "fire"

    def collide(self, enemy_x, enemy_y):
        distance = math.sqrt(((enemy_x + (50 // 2)) - self.bullet_x) ** 2 + ((enemy_y + (50 // 2)) - self.bullet_y) ** 2)
        if distance <= 25:
            self.bullet_state = "ready"
            self.bullet_y = PLAYER_Y
            self.bullet_x = -20
            return True

    def move(self, dt):
        if self.bullet_state == "fire":
            self.bullet_y -= self.bullet_speed * dt * 1000
            self.offscreen()

    def offscreen(self):
        if self.bullet_y <= 0:
            self.bullet_state = "ready"
            self.bullet_y = PLAYER_Y
            self.bullet_x = -20


class GAME:
    def __init__(self):
        mixer.music.load("back.mp3")
        mixer.music.play(-1)
        self.player = player(player_x=300, player_speed=0, image=PLAYERIMAGE)
        self.enemy = [ENEMY() for _ in range(NUMBER_OF_ENEMY)]
        self.bullet = BULLET(BULLET_SPEED)
        self.running = True


    def update_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.player_speed = PLAYER_SPEED
                if event.key == pygame.K_a:
                    self.player.player_speed = -PLAYER_SPEED
                if event.key == pygame.K_SPACE and self.bullet.bullet_state == "ready":
                    mixer.Sound("shoot.wav").play()
                    self.bullet.fire(self.player.player_x, PLAYER_Y)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_d, pygame.K_a]:
                    self.player.player_speed = 0

    def draw(self):
        score_text = SMALL_FONT.render(f"SCORE:{scoree}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        self.player.draw()
        self.bullet.draw()
        for enemyy in self.enemy:
            enemyy.draw()

    def run(self):
        while self.running:
            dt = clock.tick(60) / 1000  # FPS control & delta-time
            screen.blit(BACKGROUND, (0, 0))
            self.update_event()
            self.player.move(dt)
            self.bullet.move(dt)

            for enemyy in self.enemy:
                enemyy.move(dt)
                if self.bullet.collide(enemyy.enemy_x, enemyy.enemy_y):
                    mixer.Sound("destroyed.wav").play()
                    global scoree
                    scoree += 1
                    enemyy.respawn()

                if enemyy.did_enemy_reached_player():
                    mixer.Sound("destroyed.wav").play()
                    final_score = BIG_FONT.render(f"SCORE:{scoree}", True, (255, 255, 255))
                    screen.blit(BACKGROUND, (0, 0))
                    screen.blit(final_score, (200, 300))
                    pygame.display.update()
                    time.sleep(3)
                    self.running = False
                    break

            self.draw()
            pygame.display.update()


GAME().run()
