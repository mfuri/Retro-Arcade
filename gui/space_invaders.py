#Space Invaders Source Code
#high score in aliens destroyed
#press space to shoot and arrow keys to move or q to quit
#contributers: Michael and Mackenzie

import random
import copy
import os
from os import environ
import sys
import random
from decimal import Decimal as D
import pickle
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import *

from pygame.locals import (
   K_SPACE,
   K_RIGHT,
   K_LEFT,
   K_UP,
   K_q,
   K_ESCAPE,
   QUIT,
)

#game function
def SI_Game():
    
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500

    pygame.init()
    #subject to change
    ALIENS_INITIAL_STATE = [[36, 36], [136, 36], [236, 36], [336, 36], [436, 36],
                        [36, 86], [136, 86], [236, 86], [336, 86], [436, 86],
                        [36, 136], [136, 136], [236, 136], [336, 136], [436, 136],
                        [36, 186], [136, 186], [236, 186], [336, 186], [436, 186],
                        [36, 236], [136, 236], [236, 236], [336, 236], [436, 236]]

    #Imports keyboard controls for Pygame


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
        def update(self):
            screen.blit(self.surf, ((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20)))
    

    #Code inspiration: https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/projectiles/
    class Rocket(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super(Rocket, self).__init__()
            self.image = pygame.image.load('assets/sprites/rocket.png').convert_alpha()
            self.surf = pygame.image.load('assets/sprites/rocket.png').convert_alpha()
            self.rect = self.surf.get_rect()
            self.rect.x = x
            self.rect.y = y
        def shoot(self):
            self.rect.y -= 2
        def update(self):
            if self.rect.y < 500 and self.rect.y > 0:
                self.rect.y += -2
            else:
                self.kill()
            screen.blit(self.surf, (self.rect.x,self.rect.y)) 

    class Background:
        def __init__(self, width, height):
            pygame.init()
            self.width = width
            self.height = height
            self.screen = pygame.display.set_mode((width,height))
            self.clock = pygame.time.Clock()

    class Alien(pygame.sprite.Sprite):
        def __init__(self):
            super(Alien, self).__init__()
            #want to make each row have different color aliens
            self.blue_alien_image = pygame.image.load('assets/sprites/blue_alien.png').convert_alpha()
            self.green_alien_image = pygame.image.load('assets/sprites/green_alien.png').convert_alpha()
            self.orange_alien_image = pygame.image.load('assets/sprites/orange_alien.png').convert_alpha()
            self.purple_alien_image = pygame.image.load('assets/sprites/purple_alien.png').convert_alpha()
            self.color_list = [self.blue_alien_image, self.green_alien_image, self.orange_alien_image, self.purple_alien_image]
            self.rect = self.blue_alien_image.get_rect()
            self.level_list = []

        def create_alien(self, alien_list, x, y, alien_color):
            #need to randomize the board 
            self.rect.x = x
            self.rect.y = y
            self.rect = alien_color.get_rect()
            return self

        
        def create_alien_list(self, alien_list):
            temp_list = self.color_list.copy()
            alien_color = random.choice(temp_list)
            j = 0

            for i in range(0, 20):
                alien = Alien()
            
                if (j == 5):
                    alien_color = random.choice(temp_list)
                    j = 0 
                    temp_list.remove(alien_color)
                j += 1
                self.level_list.append(alien_color)   
                alien_list.append(alien_color.get_rect(midbottom = (ALIENS_INITIAL_STATE[i][0],ALIENS_INITIAL_STATE[i][1])))

        def draw_alien(self, aliens_list):
            i = 0
            #SOMETIMES A LITTLE WONKY BUT WILL DO FURTHER TESTING
            for alien in aliens_list:
                screen.blit(self.level_list[i], alien)
                i += 1
                #list of aliens, when an alien gets hit by rocket
                #remove it from list
        def move_aliens(self, alien_list, value):
            for alien in alien_list:
                alien.centery += value
            return alien_list 

        def rocket_collision(self, alien_list, rocket_list):
            #checks if alien collides with rocket
            i = 0
            if (len(alien_list) != 0):
                for alien in alien_list:
                    for rocket in rocket_list:
                        if rocket.rect.colliderect(alien):
                            pygame.mixer.Sound.play(kill_sound)
                            #Value Error here
                            alien_list.remove(alien)
                            rocket.kill()
                            self.level_list.remove(self.level_list[i])
                    i += 1
        def screen_collision(self, alien_list):
            for alien in alien_list:
                if (alien.midbottom[1] >= (SCREEN_HEIGHT - 70)):
                    return True
            return False

    #Draws Welcome Message
    def welcome_overlay():
        welcome_font = pygame.font.Font('assets/fonts/A-Space.otf', 18)
        welcome_text = welcome_font.render("Press Space to Start (Q or ESC to Quit)", True, (255,255,255))
        welcome_rect = welcome_text.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)))
        screen.blit(welcome_text, welcome_rect)

    def continue_overlay(level):
        continue_font = pygame.font.Font('assets/fonts/A-Space.otf', 18)
        continue_text = continue_font.render("Space to Continue (Q or ESC to Quit)", True, (255,255,255))
        continue_rect = continue_text.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)-20))
        if (level > 0):
            level_text = continue_font.render("You cleared level " + str(level) + "!", True, (255,255,255))
            level_rect = level_text.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)+20))
            screen.blit(level_text, level_rect)
        screen.blit(continue_text,continue_rect)

    def lose_overlay(level):
        lose_font = pygame.font.Font('assets/fonts/A-Space.otf', 18)
        lose_text = lose_font.render("You Lose", True, (255,255,255))
        lose_rect = lose_text.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)-20))
        if (level > 0):
            level_text = lose_font.render("You lost at level " + str(level) + ".", True, (255,255,255))
            level_rect = level_text.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)+20))
            screen.blit(level_text, level_rect)
        screen.blit(lose_text,lose_rect)
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    bg = Background(SCREEN_WIDTH,SCREEN_HEIGHT)
    ship = Ship()

    #Sounds
    #Source: https://opengameart.org/content/512-sound-effects-8-bit-style
    shoot_sound = pygame.mixer.Sound("assets/sounds/space_laser.wav")
    kill_sound = pygame.mixer.Sound("assets/sounds/space_kill.wav")
    death_sound = pygame.mixer.Sound("assets/sounds/space_death.wav")
    error_sound = pygame.mixer.Sound("assets/sounds/space_error.wav")

    #Sets ship location
    ship.rect.x = SCREEN_WIDTH / 2 - 12   # go to x
    ship.rect.y = SCREEN_HEIGHT - 50  # go to y
    player_list = pygame.sprite.Group()
    player_list.add(ship)

    #Flips display
    pygame.display.flip()

    #Create List of Aliens
    # alien = Alien()
    # aliens = []
    # alien.create_alien_list(aliens)

    #Create list of rockets
    rockets = []

    MOVEALIENS = pygame.USEREVENT
    time = 1500
    #aliens move every 1.5 seconds
    pygame.time.set_timer(MOVEALIENS, time)

    rocket_list = pygame.sprite.Group()

    running = True
    start_screen = True
    move_value = 1
    level = 0
    old_level = 0 
    highest_score = 0

    while True:
        alien = Alien()
        aliens = []
        alien.create_alien_list(aliens)
        while start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
                    pygame.quit()
                    return level
                    #sys.exit()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    level = 0
                    start_screen = False
                    running = True
                    move_value = 1
                elif event.type == KEYDOWN and (event.key != K_SPACE or event.key != K_ESCAPE or event.key != K_q):
                    pygame.mixer.Sound.play(error_sound)
                    #Will play error sound when invaid key is pressed
            screen.fill((0,0,0))
            welcome_overlay()
            pygame.display.flip()
        while running:
            #as level increases, increase move_value by 1 as well
            keys = pygame.key.get_pressed()
            screen.fill((0,0,0))
            screen.blit(ship.surf,ship.rect)
            alien.draw_alien(aliens)
        
            #Changed implementation of rockets to sprite group
            rocket_list.update()
            rocket_list.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
                    pygame.quit()
                    if level + 1 >= highest_score:
                        return level + 1
                    #sys.exit()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    rocket = Rocket(ship.rect.x+11, ship.rect.y)
                    rocket_list.add(rocket)
                    rocket_list.draw(screen)

                    pygame.mixer.Sound.play(shoot_sound)
                if event.type == MOVEALIENS:
                    alien.move_aliens(aliens, move_value) 
            #check collision

            alien.rocket_collision(aliens,rocket_list)
            if alien.screen_collision(aliens):
                running = False

            #Checks if lost
            #ship.check_alive(aliens)
            if (running == False):
                print("You Lose on Level: " + str(level+1))
                if level >= highest_score:
                    highest_score = level
                lose_screen = True

            if len(aliens) == 0:
                next_level = True
                level += 1
                if level >= highest_score:
                    highest_score = level
                while next_level:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
                            pygame.quit()
                            if (old_level >= level):
                                return old_level
                            else:
                                return level
                            #sys.exit()
                        elif event.type == KEYDOWN and event.key == K_SPACE:
                            if (old_level <= level):
                                old_level = level
                            next_level = False
                    continue_overlay(level)
                    pygame.display.flip()
                move_value += 4
                alien.create_alien_list(aliens)
                rocket_list.empty()
                ship.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20)
                pygame.display.flip()


            #Press and hold arrow keys allow ship to move calling move functions
            if keys[pygame.K_LEFT]:
                ship.move_left()
            if keys[pygame.K_RIGHT]:
                ship.move_right()    
        while lose_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
                    pygame.quit()
                    return highest_score
                    #sys.exit()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    level = 0
                    start_screen = True
                    lose_screen = False
                elif event.type == KEYDOWN and (event.key != K_SPACE or event.key != K_ESCAPE or event.key != K_q):
                    pygame.mixer.Sound.play(error_sound)
                    #Will play error sound when invaid key is pressed
            screen.fill((0,0,0))
            lose_overlay(level+1)
            pygame.display.flip()        