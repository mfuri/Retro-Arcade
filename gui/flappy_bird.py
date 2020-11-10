#Flappy Bird Source Code
#high score should be number of seconds
#press space to continue or q to quit
#contributers: Michael and Mackenzie
import random
import os
from os import environ
import sys
import random
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import *
import pygame.freetype

def Flappy_Game():
    #Imports keyboard controls for Pygame
    from pygame.locals import (
        K_SPACE,
        K_q,
        K_ESCAPE,
        QUIT,
    )

    pygame.init()

    #Grabs font from file
    score_font = pygame.font.Font('assets/fonts/Corporation_Games.otf', 42)

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
            self.rect.y -= 80
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
            self.rect.center = (SCREEN_WIDTH / 2, 475)

    class Pipe(pygame.sprite.Sprite):
        def __init__(self):
            #create pipe
            self.pipe_image = pygame.image.load('assets/sprites/spear.png')

        def create_new_pipe(self):
            pipe_heights = [350, 300, 250, 200, 180]
            bottom_pipe = random.choice(pipe_heights)
            top_pipe = bottom_pipe - 150
            new_top_pipe = self.pipe_image.get_rect(midbottom = (500, top_pipe))
            new_bottom_pipe = self.pipe_image.get_rect(midtop = (500, bottom_pipe))

            return new_top_pipe, new_bottom_pipe
        
        def move_pipes(self, pipes):
            for pipe in pipes:
                pipe.centerx -= 5
            return pipes

        def draw_pipes(self, pipes):
            for pipe in pipes:
                if(pipe.bottom >= 500):
                    screen.blit(self.pipe_image, pipe)
                else:
                    flipped_pipe = pygame.transform.flip(self.pipe_image, False, True)
                    screen.blit(flipped_pipe, pipe)
                    
        def check_collision(self, pipes, bird):
            for pipe in pipes:
                if bird.rect.colliderect(pipe):
                    return True
                if pipe.centerx <= 0:
                    pipes.remove(pipe)
            return False



    # Source: https://opensource.com/article/20/1/add-scorekeeping-your-python-game
    # Function to draw score on screen   
    def stats(score):
        outline = pygame.font.Font('assets/fonts/Corporation_Games.otf', 42)
        text = score_font.render(score, True,  (255,255,255))
        text_outline = outline.render(score, True,  (0,0,0))
        text_rect = text.get_rect(center = ((SCREEN_WIDTH / 2), 48))
        outline_rect = text_outline.get_rect(center = ((SCREEN_WIDTH / 2) + 3, 51))
        screen.blit(text_outline, outline_rect)
        screen.blit(text, text_rect)


    def lose(score):
        outline = pygame.font.Font('assets/fonts/KarmaFuture.ttf', 42)
        flap = " flaps"
        if (int(score) == 1):
            flap = " flap"
        text = outline.render("You lose: " + score + flap, True,  (255,255,255))
        text_outline = outline.render("You lose: " + score + flap, True,  (0,0,0))
        text_rect = text.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)))
        outline_rect = text_outline.get_rect(center = ((SCREEN_WIDTH / 2) + 3, (SCREEN_HEIGHT / 2)+3))
        screen.blit(text_outline, outline_rect)
        screen.blit(text, text_rect)

    #Draws welcome message
    def welcome_message():
        welcome_font = pygame.font.Font('assets/fonts/KarmaFuture.ttf', 24)
        welcome_text = welcome_font.render("Press Space to Start (Q or ESC to Quit)", True, (255,255,255))
        welcome_outline = welcome_font.render("Press Space to Start (Q or ESC to Quit)", True, (0,0,0))
        welcome_rect = welcome_text.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)-110))
        outline_rect = welcome_outline.get_rect(center = ((SCREEN_WIDTH/2) + 2,(SCREEN_HEIGHT / 2)-108))
        screen.blit(welcome_outline, outline_rect)
        screen.blit(welcome_text, welcome_rect)


    #Creates sounds to be used in-game
    flap_sound = pygame.mixer.Sound("assets/sounds/flap.wav")
    death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
    error_sound = pygame.mixer.Sound("assets/sounds/error2.wav")
    restart_sound = pygame.mixer.Sound("assets/sounds/restart.wav")

    #Creates timer and screen objects    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    #game running variable
    running = True

    #instantiates background image object
    bg = Background()

    #Instantiate enemies
    base = Base()
    #pipe = Pipe(0)

    enemy_list = pygame.sprite.Group()
    enemy_list.add(base)

    #Initializes player and assigns player class
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    #initializes pipe
    pipe = Pipe()
    pipes = []
    SPAWNPIPE = pygame.USEREVENT

    #spawns pipe every 1.25 seconds
    pygame.time.set_timer(SPAWNPIPE, 1250)

    screen.blit(player.surf, player.rect)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #Flips display
    pygame.display.flip()
    pressed_keys = pygame.key.get_pressed()

    flappy = True
    points = 0
    while flappy:
        player = Player()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        points = 0

        running = True
        #Press Space to Start Loop
        while running:
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

            #loads background image into game
            screen.fill([255, 255, 255])
            screen.blit(bg.image, bg.rect)
            screen.blit(player.surf, ((SCREEN_WIDTH / 2)-17, player.rect.y))
            screen.blit(base.image, base.rect)
            #pipe.draw(screen)
            #Welcome image
            welcome_message()
            #screen.blit(welcome.image,welcome.rect)
            pygame.display.flip()

        running = True
        #main game loop
        #game loop
        
        while running:
            #turn false when user hits pipe or the ground or the top of the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Controls -- Space = jump; q, escape = quit
                if event.type == KEYDOWN and event.key == K_SPACE:
                    player.jump()
                    points += 1
                    pygame.mixer.Sound.play(flap_sound)
                elif event.type == KEYDOWN and (event.key == K_q or K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == SPAWNPIPE:
                    pipes.extend(pipe.create_new_pipe())
                    

            player.update()
            #pipe.check_collision(pipes, player)
            if pipe.check_collision(pipes, player):
                pygame.mixer.Sound.play(death_sound)
                lose(str(points))
                running = False

            if player.alive == False:
                pygame.mixer.Sound.play(death_sound)
                lose(str(points))
                running = False
            #loads background image into game
            screen.fill([255, 255, 255])
            screen.blit(bg.image, bg.rect)
            player.gravity()
            screen.blit(player.surf, ((SCREEN_WIDTH / 2)-17, player.rect.y))
            screen.blit(base.image,base.rect)

            #draw pipes
            pipe.draw_pipes(pipes)
            pipe.move_pipes(pipes)
            stats(str(points))
            pygame.display.flip()
            
        running = True
        while running:
            #turn false when user hits green pipe or the ground or the top of the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    flappy = False
            # Controls -- Space = jump; q, escape = quit
                if event.type == KEYDOWN and event.key == K_SPACE:
                    running = False
                    flappy = True
                    player.alive = True
                    pygame.mixer.Sound.play(restart_sound)
                elif event.type == KEYDOWN and (event.key == K_q or K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                    running = False
                    flappy = False
            #loads background image into game
            screen.fill([255, 255, 255])
            screen.blit(bg.image, bg.rect)
            screen.blit(base.image,base.rect)
            lose(str(points))
            pygame.display.flip()
            pipes = []
    print(points)
    #exits game window
    pygame.quit()

    #code source: https://realpython.com/pygame-a-primer/
    #code source: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
    #sounds source: https://opengameart.org/content/512-sound-effects-8-bit-style
    #numbers source: https://www.flaticon.com/home
    #pipe code reference: https://www.youtube.com/watch?v=UZg49z76cLw
