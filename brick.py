import pygame

# Sprite是pygame本身自带的一个精灵。但是这个类的功能比较少，因此我们新建一个类对其继承
class Brick(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/1级方块.png").convert_alpha()
        self.image2 = pygame.image.load("images/2级方块.png").convert_alpha()
        self.image3 = pygame.image.load("images/3级方块.png").convert_alpha()
        # 设置中间变量
        self.image4 = pygame.image.load("images/3级方块.png").convert_alpha()
        self.curimage = self.image4

        self.rect = self.image1.get_rect()
        self.mask = pygame.mask.from_surface(self.image1)


    def change_position(self, left, top):
        self.rect.left = left
        self.rect.top = top
