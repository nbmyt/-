import pygame
import board

class Ball(pygame.sprite.Sprite):
    def __init__(self, boards):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/球.png").convert_alpha()
        self.ball_speed = [3, -3]
        self.is_hit = False
        self.is_speedupball = False
        self.rect = self.image1.get_rect()

        self.rect.left, self.rect.bottom = boards.rect.left + (boards.rect.width - self.rect.width) / 2,boards.rect.top

        self.mask = pygame.mask.from_surface(self.image1)