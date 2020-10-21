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


class Game:
    screen = None
    aliens = []
    rockets = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        done = False

        hero = Ship( width / 2, height - 20)
        generator = Generator(self)
        rocket = None

        while not done:
            if len(self.aliens) == 0:
                self.displayText("VICTORY ACHIEVED")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:  # sipka doleva
                hero.x -= 2 if hero.x > 20 else 0  # leva hranice plochy
            elif pressed[pygame.K_RIGHT]:  # sipka doprava
                hero.x += 2 if hero.x < width - 20 else 0  # prava hranice

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.rockets.append(Rocket(self, hero.x, hero.y))

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > height):
                    self.lost = True
                    self.displayText("YOU DIED")

            for rocket in self.rockets:
                rocket.draw()

            if not self.lost: hero.draw()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))


class Alien:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.size = 30

    def draw(self):
        pygame.draw.rect(self.game.screen,  # renderovací plocha
                         (81, 43, 88),  # barva objektu
                         pygame.Rect(self.x, self.y, self.size, self.size))
        self.y += 0.05

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + self.size and
                    rocket.x > self.x - self.size and
                    rocket.y < self.y + self.size and
                    rocket.y > self.y - self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ship, self).__init__()
        self.x = x
        self.y = y
        self.surf = pygame.image.load('assets/sprites/ship.png').convert_alpha()

    def draw(self):
        self.rect = self.surf.get_rect()


class Generator:
    def __init__(self, game):
        margin = 30  # mezera od okraju obrazovky
        width = 50  # mezera mezi alieny
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2), width):
                game.aliens.append(Alien(game, x, y))

        # game.aliens.append(Alien(game, 280, 50))


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,  # renderovací plocha
                         (254, 52, 110),  # barva objektu
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 2 


if __name__ == '__main__':
    game = Game(500, 500)