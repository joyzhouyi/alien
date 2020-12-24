import pygame
from pygame.sprite import Sprite


class Boom(Sprite):
    def __init__(self, alien, screen, ai_settings):
        super(Boom, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载外星人图像，并设置其rect属性
        if alien.rect.height==40:
          self.image = pygame.image.load('images/boom1.png')
        elif alien.rect.height==80:
            self.image = pygame.image.load('images/boom11.png')
        self.rect = self.image.get_rect()
        self.alien=alien
        # 每个外星人最初都在屏幕的左上角附近
        self.rect.x = alien.rect.x
        self.rect.y = alien.rect.y
        self.x=self.rect.x
        self.y=self.rect.y
        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.curI = 0
        self.targetI = 9

    def blitme(self):
        """在指定的位置绘制外星人"""
        if self.alien.rect.height==40 and self.curI <=self.targetI:
            self.screen.blit(self.image, self.rect)
        elif self.alien.rect.height==80 and self.curI <=self.targetI+5:
            self.screen.blit(self.image, self.rect)
    def update(self, *args):
        if self.alien.rect.height==40:
            self.image = pygame.image.load('images/boom'+str(int(self.curI/3+1))+'.png')
        elif self.alien.rect.height==80:
            self.image = pygame.image.load('images/boom1' + str(int(self.curI / 3 + 1)) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.curI = self.curI + 1