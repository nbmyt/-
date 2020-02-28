import pygame
import random


class Reward(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/保护.png").convert_alpha()
        self.image2 = pygame.image.load("images/板加长.png").convert_alpha()
        self.image3 = pygame.image.load("images/球数+1.png").convert_alpha()
        self.image4 = pygame.image.load("images/球速度+5(10s).png").convert_alpha()
        # 设置中间变量
        self.image5 = pygame.image.load("images/球速度+5(10s).png").convert_alpha()

        self.rect = self.image1.get_rect()

        self.current_image = self.image5

        self.mask = pygame.mask.from_surface(self.image1)

    def generate_reward(self):
        rand = random.randint(1, 200)
        # 无敌
        if rand <= 5:
            self.current_image = self.image1
        # 板加长(10s)
        elif 6 <= rand <= 10:
            self.current_image = self.image2
        # 球数+1
        elif 11 <= rand <= 15:
            self.current_image = self.image3
        # 球速度+5(10s)
        elif 16 <= rand <= 20:
            self.current_image = self.image4
        else:
            self.current_image = self.image5
