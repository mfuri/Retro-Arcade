import pygame
import sys
import time
import random
import pygame.locals
from os import environ #importing neccessary libraries
from pygame.locals import *
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
#definition for the snake game and neccessary features used through program
def Snake():
    FPS = 15 #controlling how fast the snake should be going
    pygame.init() #initializing pygame
    fpsClock = pygame.time.Clock()
    red = (255, 0, 0)
    green = (99, 255, 32)
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    black = (0, 0, 0)
    white = (255, 255, 255)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 40)
    GRIDSIZE = 10
    GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
    GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
    #runningSound = pygame.mixer.sound("[ONTIVA.COM] 8-Bit RPG Music - Dance-off _ Original Composition-64k.wav")
    pygame.mixer.music.load("assets/sounds/[ONTIVA.COM] 8-Bit RPG Music - Dance-off _ Original Composition-64k.wav")
    pygame.mixer.music.play(-1)
    deathSound = pygame.mixer.Sound("assets/sounds/deathsound.wav")
    eatSound = pygame.mixer.Sound("assets/sounds/levelup.wav")
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    screen.blit(surface, (0, 0))

    #defining the draw box to open the window for the game
    def draw_box(surf, color, pos):
        r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surf, color, r)

    #definition for the start screen
    def startScreen():
        font = pygame.font.Font(None, 36)
        text = font.render("Press Space to Start", True, (255, 255, 255))
        window = font.render("Press Space to Start (Q or ESC to Quit)", True, (0, 0, 0))
        tRect = text.get_rect(center=((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 110))
        oect = window.get_rect(center=((SCREEN_WIDTH / 2) + 2, (SCREEN_HEIGHT / 2) - 108))
        screen.blit(window, oect)
        screen.blit(text, oect)

    #definition for the screen when the player loses
    def loseScreen():
        font = pygame.font.Font(None, 36)
        text = font.render("Press Space to Continue", True, (255, 255, 255))
        window = font.render("Press Space to Continue (Q or ESC to Quit)", True, (0, 0, 0))
        tRect = text.get_rect(center=((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 110))
        oect = window.get_rect(center=((SCREEN_WIDTH / 2) + 2, (SCREEN_HEIGHT / 2) - 108))
        screen.blit(window, oect)
        screen.blit(text, oect)

    #definition for the snake class
    class Snake(object):
        def __init__(self):
            self.lose()
            self.color = (green)

        #definition to get the spot in which the snakes head is
        def get_head_position(self):
            return self.positions[0]

        #definition for function that executes when player loses
        def lose(self):
            self.length = 1
            self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
            self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
            pygame.mixer.Sound.play(deathSound)
            pygame.mixer.music.stop()
            print("Death to the snake")

        #definition to award points for when a apple is eaten
        def point(self, pt):
            if self.length > 2 and (pt[0] * -1, pt[1] * -1) == self.direction:
                print(pt[0] * -1, pt[1] * -1)
                self.lose()
                return False
            else:
                self.direction = pt
                return True
        #definition for function that makes snake move
        #Code inspired from this video https://www.youtube.com/watch?v=9bBgyOkoBQ0
        def move(self):
            cur = self.positions[0]
            x, y = self.direction
            new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
            if len(self.positions) > 2 and new in self.positions[2:]:
                self.lose()
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()
        #definition to draw the snake
        def draw(self, surf):
            for p in self.positions:
                draw_box(surf, self.color, p)

    #defintion for the apple class
    class Apple(object):
        def __init__(self):
            self.position = (0, 0)
            self.color = (red)
            self.randomize()
        #defintion to draw the apple
        def draw(self, surf):
            draw_box(surf, self.color, self.position)
        #defintion to put the apple in a random spot on screen
        def randomize(self):
            self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)
    #definition to check if the snake has eaten an apple
    def check_eat(snake, apple):
        if snake.get_head_position() == apple.position:
            snake.length = snake.length + 1
            apple.randomize()
            pygame.mixer.Sound.play(eatSound)
            pygame.mixer.music.stop()
            print("Snake has eaten an apple")
    #setting variables to class objects and boolean flags
    player = Snake()
    goal = Apple()
    start = True
    lost = False
    highest_score = 0
    #do this when start is true, navigate the game
    while True:
        player = Snake()
        goal = Apple()
        while start:
            surface.fill(black)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        start = False
                        running = True
                    elif event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
                        pygame.display.quit()
                        if player.length > highest_score:
                            highest_score = player.length
                        return highest_score
                if event.type == QUIT:
                    pygame.quit()
                    if player.length > highest_score:
                        highest_score = player.length
                    return highest_score
                pygame.display.update()

            font = pygame.font.Font(None, 30)
            text = font.render("Press Space to Start", True, white, black)
            tRect = text.get_rect(center=((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 85))
            screen.blit(text, tRect)
            pygame.display.flip()
        #while the game is running, navigate the game fairly
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if not player.point(UP):
                            running = False
                            lost = True
                            break
                    elif event.key == K_DOWN:
                        if not player.point(DOWN):
                            running = False
                            lost = True
                            break
                    elif event.key == K_LEFT:
                        if not player.point(LEFT):
                            running = False
                            lost = True
                            break
                    elif event.key == K_RIGHT:
                        if not player.point(RIGHT):
                            running = False
                            lost = True
                            break
                if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
                    pygame.mixer.Sound.play(deathSound)
                    pygame.mixer.music.stop()
                    pygame.quit()
                    if player.length > highest_score:
                        highest_score = player.length
                    return highest_score
            #if the player loses, execute this code block
            if lost:
                player = Snake()
                goal = Apple()
                break
            #do this in case of a new high score
            if player.length > highest_score:
                highest_score = player.length
            surface.fill(black)

            check_eat(player, goal)
            player.draw(surface)
            goal.draw(surface)
            player.move()
            #following code sets the windows properly and updates it

            font = pygame.font.Font(None, 36)
            text = font.render(str(player.length), 1, (white))
            textpos = text.get_rect()
            textpos.centerx = 450
            surface.blit(text, textpos)
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            pygame.display.update()
            fpsClock.tick(FPS)
        #entire this while loop in case we lose
        while lost:
            surface.fill(black)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        start = True
                        lost = False
                if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
                    pygame.quit()
                    if player.length > highest_score:
                        highest_score = player.length
                    return highest_score
            #print a loss screen
            font = pygame.font.Font(None, 30)
            text = font.render("You lose. Press Space to Continue", 1, white, black)
            tRect = text.get_rect(center=((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 110))
            screen.blit(text, tRect)
            pygame.display.flip()
    pygame.display.quit()
#ending the game
#code inspiration for moving https://www.youtube.com/watch?v=9bBgyOkoBQ0