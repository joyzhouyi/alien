import pygame
from pygame.sprite import Sprite


class Blood(Sprite):
    """一个对飞船反射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen, alien):
        """在飞船所处的位置创建一个子弹对象"""
        super(Blood, self).__init__()
        self.screen = screen
        # 在（0，0）处创建一个表示子弹的矩形，在设置正确的位置
        # 血条下面的矩形
        self.rect1 = pygame.Rect(0, 0, alien.rect.width - 10, ai_settings.blood_height)
        self.rect1.x = alien.rect.x + 5
        self.rect1.y = alien.rect.y - 10
        # 血条上面的矩形
        self.rect2 = pygame.Rect(0, 0, alien.rect.width - 10, ai_settings.blood_height)
        self.rect2.x = alien.rect.x + 5
        self.rect2.y = alien.rect.y - 10
        self.alien = alien
        # 存储用小数（浮点数）表示的子弹位置
        self.color1 = ai_settings.blood_color1  # 红色
        self.color2 = ai_settings.blood_color2  # 蓝色

    def update(self):
        """血条的位置随外星人的变化而变"""
        self.rect1.x = self.alien.rect.x + 5
        self.rect1.y = self.alien.rect.y - 10
        self.rect2.x = self.alien.rect.x + 5
        self.rect2.y = self.alien.rect.y - 10

    def resetBloodLength(self, ai_settings):
        if self.alien.rect.width == 40:
            self.rect2.width = self.alien.blood / ai_settings.alien_blood * (self.alien.rect.width - 10)
        else:
            self.rect2.width = self.alien.blood / ai_settings.boss_blood * (self.alien.rect.width - 10)

    def draw_bullet(self):
        """在屏幕上绘制血条"""
        pygame.draw.rect(self.screen, self.color1, self.rect1)
        pygame.draw.rect(self.screen, self.color2, self.rect2)
