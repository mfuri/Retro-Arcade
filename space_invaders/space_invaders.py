#Space Invaders Source Code
#high score in aliens destroyed
#press space to shoot and arrow keys to move or q to quit
#contributers: Michael and Mackenzie
import random
import os
from os import environ
import sys
import random
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

pygame.init()

#Imports keyboard controls for Pygame
from pygame.locals import (
    K_SPACE,
    K_RIGHT,
    K_LEFT,
    K_UP,
    K_q,
    K_ESCAPE,
    QUIT,
)

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super(Ship, self).__init__()
        self.surf = pygame.image.load('assets/sprites/ship.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20)
        self.movey = 0
        self.movex = 0
        self.alive = True
    def handle_keys(self):
        key = pygame.key.get_pressed()
    def move_left(self):
        movex -= 5
    def move_left(self):
        movex += 5
    #Checks if sprite collides with enemies
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.alive = False

class Background:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

bg = Background(SCREEN_WIDTH,SCREEN_HEIGHT)
ship = Ship()

#Flips display
pygame.display.flip()
pressed_keys = pygame.key.get_pressed()

while True:
    level = 0
    screen.blit()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            player.jump()
            pygame.mixer.Sound.play(flap_sound)
            running = False
        elif event.type == KEYDOWN and event.key != K_SPACE:
            pygame.mixer.Sound.play(error_sound)