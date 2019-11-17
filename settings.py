# -*- coding: utf-8 -*-


class Settings:
    """ 存储《外星人入侵》的所有设置的类 """

    def __init__(self):
        """ 初始化游戏的设置 """
        #  屏幕设置
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        #  子弹设置
        self.bullet_image = 'images/bullet.png'
        self.bullet_speed_factor = 1
        self.bullet_width = 30
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 30

        #  飞船设置
        self.ship_speed_factor = 1
        self.ship_image = 'images/ship.png'
        self.ship_limit = 3

        #  外星人设置
        self.alien_image = 'images/alien.png'
        self.alien_speed_factor = 2
        self.fleet_drop_speed = 50
        # fleet_direction 为 1 表示向右移，为 -1 表示向左移
        self.fleet_direction = 1

