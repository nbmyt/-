import base64
import pygame
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/球.jpg").convert_alpha()
        self.rect = self.image.fill(color, None, BLEND_ADD)
        self.rect.topleft = initial_position

pygame.init()
screen = pygame.display.set_mode([350, 350])

ball = Ball((255, 0, 0), (100, 100))
screen.blit(ball.image, ball.rect)
pygame.display.update()
while pygame.event.poll().type != KEYDOWN:
    pygame.time.delay(10)