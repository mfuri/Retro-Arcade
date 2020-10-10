#Flappy Bird Source Code
#high score should be number of seconds
#press space to continue or q to quit
#contributers: Michael and Mackenzie
import random
import os
from os import environ
import sys
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import *

#Imports keyboard controls for Pygame
from pygame.locals import (
    K_SPACE,
    K_q,
    QUIT,
)

pygame.init()

#Set resolution to 500x500
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

#Defines class player model, pulls sprite from assets folder
#Sprite source: https://en.wikipedia.org/wiki/Florida_State_Seminoles#/media/File:Florida_State_Seminoles_logo.svg
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('assets/sprites/our_bird.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.movey = 0
        self.movex = 0
        self.rect.y = SCREEN_WIDTH / 2
    def gravity(self):
        self.rect.y += 5
    def handle_keys(self):
        key = pygame.key.get_pressed()
        

#Defines background image, pulls image from assets folder
#Image source: https://www.flickr.com/photos/91152366@N06/21368054180/
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load('assets/sprites/background2.png')
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

#Creates timer and screen objects    
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#game running variable
running = True

#instantiates background image object
bg = Background()

#Initializes player and assigns player class
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

screen.blit(player.surf, player.rect)
for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)

#Flips display
pygame.display.flip()
pressed_keys = pygame.key.get_pressed()

jump = False

#game loop
while running:
    
    #turn false when user hits green pipe or the ground or the top of the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.update()
    #loads background image into game
    screen.fill([255, 255, 255])
    screen.blit(bg.image, bg.rect)
    #screen.blit(player.surf, player.rect)
    screen.blit(player.surf, (SCREEN_WIDTH / 2, player.rect.y))
    if event.type == KEYDOWN:
        if event.key == K_SPACE:
            jump = True
    
    if event.type == KEYUP:
        if event.key == K_SPACE:
            jump = False
        if event.key == K_q:
            pygame.quit()
            sys.exit()
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()


    player.gravity()

    pygame.display.flip()
#exits game window
pygame.quit()

#code source: https://realpython.com/pygame-a-primer/
#code source: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
#sounds source: https://opengameart.org/content/512-sound-effects-8-bit-style