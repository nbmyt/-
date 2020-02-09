#!/usr/bin/env python
# coding=utf-8

import pygame, sys

pygame.init()

size = width, height = 640, 480
# screen = pygame.display.set_mode(size, pygame.RESIZABLE)
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("打砖块")

backGround = pygame.image.load("picture/background.jpg").convert()
# backGround = pygame.image.load("picture/PYG02-ball.gif")
screen.blit(backGround, (0, 0))
fps = 300
fclock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
    fclock.tick(fps)
