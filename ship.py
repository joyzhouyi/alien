import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        """初始化飞船并社长其初始位置"""
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载飞机图片并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放到屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 在飞船的属性center中存储小数值（带浮点数的值）
        self.centerX = float(self.rect.centerx)
        self.centerY = float(self.rect.bottom)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False
        self.curC = 12
        self.targetC = 12
        self.isBoom = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船的center值，而不是rect
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            # self.rect.centerx += 1
            self.centerX += (self.ai_settings.ship_speed_factor )
        if self.moving_left and (self.rect.left > self.screen_rect.left):
            # self.rect.centerx -= 1
            self.centerX -= (self.ai_settings.ship_speed_factor )
        if self.moving_top and (self.rect.top > 80):
            self.centerY -= (self.ai_settings.ship_speed_factor )
        if self.moving_bottom and (self.rect.bottom < self.screen_rect.bottom):
            self.centerY += (self.ai_settings.ship_speed_factor )
        # 根据self.center更新rect对象
        self.rect.centerx = self.centerX
        self.rect.bottom = self.centerY
        # 更新飞船的center的值，而不是rect
        # if self.moving_right and (self.rect.right<self.screen_rect.right):

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
        if self.curC < 12:
            self.curC = self.curC + 1
            # print(self.curC)
        if self.isBoom:
            if self.curC == self.targetC:
                self.center_ship()
                self.isBoom = False

    def center_ship(self):
        """让飞船在屏幕上居中"""
        if self.curC == self.targetC:
            self.centerX = self.screen_rect.centerx
            self.centerY = self.screen_rect.bottom
            self.curC = 0
        else:
            self.centerY = 10000
            self.centerX = 10000

