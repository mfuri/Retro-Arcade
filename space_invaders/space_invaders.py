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

import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('assets/sprites/ship.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20)
        self.movey = 0
        self.movex = 0
        self.alive = True
    def handle_keys(self):
        key = pygame.key.get_pressed()
    #Checks if sprite collides with enemies
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.alive = False