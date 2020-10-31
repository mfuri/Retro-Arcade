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
        if self.rect.x >= 10:
            self.rect.x -= 5
    def move_right(self):
        if self.rect.x <= SCREEN_WIDTH - 34:
            self.rect.x += 5
    #Checks if sprite collides with enemies
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.alive = False

class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Rocket, self).__init__()
        self.surf = pygame.image.load('assets/sprites/rocket.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_rockets(self, rocket_list):
        for rocket in rocket_list:
            if rocket.rect.y == 0:
                rocket_list.remove(rocket)
            screen.blit(self.surf, rocket) 
    def shoot(self):
        self.rect.y -= 2

class Background:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        #want to make each row have different color aliens
        self.alien_image = pygame.image.load('assets/sprites/blue_alien.png').convert_alpha()
    def create_alien(self):
        self.rect = self.alien_image.get_rect()
        self.rect.x = SCREEN_WIDTH/2 - 16
        self.rect.y = SCREEN_HEIGHT/2 - 16
        #self.alien_image.get_rect()
        return self
    def draw_alien(self, aliens_list):
        for alien in aliens_list:
            screen.blit(self.alien_image, alien)
            #list of aliens, when an alien gets hit by rocket
            #remove it from list
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

bg = Background(SCREEN_WIDTH,SCREEN_HEIGHT)
ship = Ship()

#Sets ship location
ship.rect.x = SCREEN_WIDTH / 2 - 12   # go to x
ship.rect.y = SCREEN_HEIGHT - 50  # go to y
player_list = pygame.sprite.Group()
player_list.add(ship)

#Flips display
pygame.display.flip()
#keys = pygame.key.get_pressed()

#Create List of Aliens
alien = Alien()
aliens = []
aliens.append(alien.create_alien())

#Create list of rockets
rockets = []

while True:
    keys = pygame.key.get_pressed()
    rocket = Rocket(ship.rect.x, ship.rect.x)
    level = 0
    screen.fill((0,0,0))
    screen.blit(ship.surf,ship.rect)
    alien.draw_alien(aliens)
    rocket.draw_rockets(rockets)
    pygame.display.flip()
    for rocket in rockets:
        if rocket.rect.y < 500 and rocket.rect.y > 0:
            rocket.shoot()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            rockets.append(Rocket(ship.rect.x+11, ship.rect.y))
    #Press and hold arrow keys allow ship to move calling move functions
    if keys[pygame.K_LEFT]:
        ship.move_left()
    if keys[pygame.K_RIGHT]:
        ship.move_right()

            