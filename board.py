import pygame


class Board(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/板.png").convert_alpha()
        self.image2 = pygame.image.load("images/加长板.jpg").convert_alpha()
        self.current_image = self.image1#中间变量
        self.rect = self.current_image.get_rect()

        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 20
        self.mask = pygame.mask.from_surface(self.image1)

    def change_object(self, board_left):
        if self.current_image == self.image1:
            self.rect = self.image2.get_rect()
            self.current_image = self.image2
            self.rect.left, self.rect.top = board_left  , self.height - self.rect.height - 20
            self.mask = pygame.mask.from_surface(self.image2)
        else:
            self.rect = self.image1.get_rect()
            self.current_image = self.image1
            self.rect.left, self.rect.top = board_left  , self.height - self.rect.height - 20
            self.mask = pygame.mask.from_surface(self.image1)
