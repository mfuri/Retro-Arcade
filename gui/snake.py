import pygame
import sys
import time
import random
import pygame.locals
from pygame.locals import *
#environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

def Snake():
    FPS = 10
    pygame.init()
    fpsClock = pygame.time.Clock()
    red = (255, 0, 0)
    green = (99, 255, 32)
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    black = (0,0,0)
    white = (255,255,255)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 40)
    GRIDSIZE = 10
    GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
    GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
    #runningSound = pygame.mixer.sound("assets/sounds/sample.wav")
    #deathSound = pygame.mixer.sound("assets/sounds/sample2.wav")
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    screen.blit(surface, (0, 0))


    def draw_box(surf, color, pos):
        r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surf, color, r)

    def startScreen():
        font = pygame.font.Font(None, 36)
        text = font.render("Press Space to Start", True, (255,255,255))
        window = font.render("Press Space to Start (Q or ESC to Quit)", True, (0, 0, 0))
        tRect = text.get_rect(center=((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 110))
        oect = window.get_rect(center=((SCREEN_WIDTH / 2) + 2, (SCREEN_HEIGHT / 2) - 108))
        screen.blit(window, oect)
        screen.blit(text, oect)

    class Snake(object):
        def __init__(self):
            self.lose()
            self.color = (green)

        def get_head_position(self):
            return self.positions[0]

        def lose(self):
            self.length = 1
            self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
            self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

        def point(self, pt):
            if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
                return
            else:
                self.direction = pt

        def move(self):
            cur = self.positions[0]
            x,y = self.direction
            new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
            if len(self.positions) > 2 and new in self.positions[2:]:
                self.lose()
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()

        def draw(self, surf):
            for p in self.positions:
                draw_box(surf, self.color, p)


    class Apple(object):
        def __init__(self):
            self.position = (0, 0)
            self.color = (red)
            self.randomize()

        def draw(self, surf):
            draw_box(surf, self.color, self.position)

        def randomize(self):
            self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)


    def check_eat(snake, apple):
        if snake.get_head_position() == apple.position:
            snake.length = snake.length + 1
            apple.randomize()

    player = Snake()
    goal = Apple()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player.point(UP)
                elif event.key == K_DOWN:
                    player.point(DOWN)
                elif event.key == K_LEFT:
                    player.point(LEFT)
                elif event.key == K_RIGHT:
                    player.point(RIGHT)
                if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
                    pygame.quit()
                    print(player.length)
                    return player.length

            surface.fill(black)
            player.move()
            check_eat(player, goal)
            player.draw(surface)
            goal.draw(surface)
            font = pygame.font.Font(None, 36)
            text = font.render(str(player.length), 1, (white))
            textpos = text.get_rect()
            textpos.centerx = 450
            surface.blit(text, textpos)
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            pygame.display.update()
            fpsClock.tick(FPS)