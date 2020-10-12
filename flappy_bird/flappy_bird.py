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
    K_ESCAPE,
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
        self.rect.y = SCREEN_WIDTH / 2 - 60
        self.alive = True
    def gravity(self):
        self.rect.y += 3
    def handle_keys(self):
        key = pygame.key.get_pressed()
    def jump(self):
        self.rect.y -= 100
    #Checks if sprite collides with enemies
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.alive = False
        

#Defines background image, pulls image from assets folder
#Image source: https://www.flickr.com/photos/91152366@N06/21368054180/
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load('assets/sprites/background2.png')
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

#Code source: https://opensource.com/article/18/5/pygame-enemy
class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sprites/base2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, 450)


#Creates text overlay welcome message
class Welcome_Overlay(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/welcome_screen.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('assets/sprites/spear.png').convert_alpha()
        self.rect = self.surf.get_rect()
        
#Creates sounds to be used in-game
flap_sound = pygame.mixer.Sound("assets/sounds/flap.wav")
death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
error_sound = pygame.mixer.Sound("assets/sounds/error2.wav")

#Creates timer and screen objects    
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#game running variable
running = True

#instantiates background image object
bg = Background()
welcome = Welcome_Overlay()

#Instantiate enemies
base = Base()

enemy_list = pygame.sprite.Group()
enemy_list.add(base)


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

#Press Space to Start Loop
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                player.jump()
                pygame.mixer.Sound.play(flap_sound)
                running = False
            elif event.type == KEYDOWN and event.key != K_SPACE:
                pygame.mixer.Sound.play(error_sound)

    #loads background image into game
    screen.fill([255, 255, 255])
    screen.blit(bg.image, bg.rect)
    screen.blit(player.surf, ((SCREEN_WIDTH / 2)-17, player.rect.y))
    screen.blit(base.image, base.rect)

    #Welcome image
    screen.blit(welcome.image,welcome.rect)
    pygame.display.flip()

running = True
#main game loop
#game loop
while running:
    
    #turn false when user hits green pipe or the ground or the top of the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Controls -- Space = jump; q, escape = quit
        if event.type == KEYDOWN and event.key == K_SPACE:
            player.jump()
            pygame.mixer.Sound.play(flap_sound)
        elif event.type == KEYUP:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    player.update()
    if player.alive == False:
      running = False
    #loads background image into game
    screen.fill([255, 255, 255])
    screen.blit(bg.image, bg.rect)
    player.gravity()
    #screen.blit(player.surf, player.rect)
    screen.blit(player.surf, ((SCREEN_WIDTH / 2)-17, player.rect.y))
    screen.blit(base.image,base.rect)
    

    pygame.display.flip()
#exits game window
pygame.quit()

#code source: https://realpython.com/pygame-a-primer/
#code source: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
#sounds source: https://opengameart.org/content/512-sound-effects-8-bit-style
#numbers source: https://www.flaticon.com/home