# -*- coding: utf-8 -*-
import pygame


class Ship:
    def __init__(self, screen, setting):
        """ 初始化飞船并设置其初始位置 """
        self.screen = screen
        self.moving_right = False
        self.moving_left = False
        self.ship_speed_factor = setting.ship_speed_factor

        #  加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(setting.ship_image)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #  将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        """ 在指定位置绘制飞船 """
        self.screen.blit(self.image, self.rect)

    def move_right(self):
        """ 飞船向右移动一格 """
        if self.moving_right is False:
            self.moving_left = False
            self.moving_right = True
        if self.rect.right + self.ship_speed_factor < self.screen_rect.right:
            self.rect.centerx += self.ship_speed_factor

    def move_left(self):
        """ 飞船向左移动 """
        if self.moving_left is False:
            self.moving_left = True
            self.moving_right = False
        if self.rect.left - self.ship_speed_factor > self.screen_rect.left:
            self.rect.centerx -= self.ship_speed_factor

    def move_left_stop(self):
        """ 飞船停止左移动 """
        self.moving_left = False

    def move_right_stop(self):
        """ 飞船停止右移动 """
        self.moving_right = False

    def update(self):
        """ 飞船保持当前状态(移动方向) """
        if self.moving_left:
            self.move_left()
        if self.moving_right:
            self.move_right()

    def center_ship(self):
        """ 让飞船在屏幕上居中 """
        self.rect.centerx = self.screen_rect.centerx

