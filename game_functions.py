# -*- coding:utf-8-*-
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ 响应按键 """
    if event.key == pygame.K_RIGHT:
        ship.move_right()
    elif event.key == pygame.K_LEFT:
        ship.move_left()
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """ 如果还没有到达限制，就发射一颗子弹 """
    # 创建新子弹，并将其加入到编组 bullets 中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """ 响应松开 """
    if event.key == pygame.K_RIGHT:
        ship.move_right_stop()
    elif event.key == pygame.K_LEFT:
        ship.move_left_stop()


def check_events(ai_settings, screen, stats, play_button, ship, aliens,
                 bullets):
    """ 监听是否有键盘/鼠标事件发生 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #  键盘被按下
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        #  键盘弹起
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """ 在玩家单击 Play 按钮时开始新游戏 """
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        #  重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #  清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #  创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, ship, aliens, bullets,
                  play_button):
    """ 更新屏幕上的图像，并切换到新屏幕 """
    #  更新背景颜色\飞船\外星人
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

    #  在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #  如果游戏处于非活动状态，就绘制 Play 按钮
    if not stats.game_active:
        play_button.draw_button()

    #  让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """ 更新子弹位置 """
    bullets.update()
    #  删除已消失的子弹
    #  !!在 for 循环中，不应从列表或编组中删除条目，因此必须遍历编组的副本
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """ 响应子弹和外星人的碰撞 """
    #  删除发生碰撞的子弹和外星人（多对多）
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """ 获取一行能够容纳的外星人数量 """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ 创建一个外星人到外星人队列中 """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """ 计算屏幕可容纳多少行外星人 """
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_fleet(ai_settings, screen, ship, aliens):
    """ 创建外星人群 """
    #  创建一个外星人，并计算一行可容纳多少个外星人
    #  外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    #  创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #  创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """ 有外星人到达边缘时采取相应的措施 """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ 将整群外星人下移，并改变它们的方向 """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """ 响应飞船被外星人撞到 """
    if stats.ships_left > 0:
        #  将 ships_left 减 1
        stats.ships_left -= 1
        #  清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #  创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #  暂停
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """ 检查是否有外星人到达了屏幕底端 """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #  像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """ 检查是否有外星人位于屏幕边缘，并更新整群外星人的位置 """
    check_fleet_edges(ai_settings, aliens)
    #  可以通过group一次性调用所有alien的方法
    aliens.update()

    #  检测外星人和飞船之间的碰撞(单对多)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
