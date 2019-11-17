# -*- coding: utf-8 -*-

import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
#  pygame.sprite.Group 类类似于列表，但提供了有助于开发游戏的额外功能


def run_game():
    """ 主游戏入口 """
    pygame.display.set_caption("Alien Invasion")
    #  初始化设置
    ai_settings = Settings()
    #  创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    #  构造背景
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    #  创建一个用于存储子弹的编组\存储外星人的编组
    bullets = Group()
    aliens = Group()

    #  创建外星人群\飞船\Play 按钮
    ship = Ship(screen, ai_settings)
    gf.create_fleet(ai_settings, screen, ship, aliens)
    play_button = Button(ai_settings, screen, "Play")

    #  开始游戏主循环
    while True:
        #  监听处理键盘鼠标事件
        gf.check_events(ai_settings, screen, stats, play_button, ship,
                        aliens, bullets)
        if stats.game_active is True:
            #  更新飞船\外星人组\子弹组状态
            ship.update()
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
        else:
            play_button.draw_button()
        #  让最近绘制的屏幕可见
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets,
                         play_button)


run_game()
