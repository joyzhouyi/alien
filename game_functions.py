import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from boom import Boom
from boss import Boss
import random
from blood import Blood


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, bloods):
    """响应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, screen, ai_settings, bullets, stats, play_button)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship, screen, ai_settings, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y,
                              bloods)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, booms, bloods):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for blood in bloods.sprites():
        blood.draw_bullet()
    ship.blitme()
    for boom in booms:
        boom.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_keydown_events(event, ship, screen, ai_settings, bullets, stats, play_button):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_top = True
    elif event.key == pygame.K_DOWN:
        ship.moving_bottom = True
    elif event.key == pygame.K_SPACE:
        if stats.game_active == True:
            fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        if stats.game_active == True:
            stats.game_active = False
            play_button.resSetMsg("Continue")


def check_keyup_events(event, ship, screen, ai_settings, bullets):
    """响应按键松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_top = False
    elif event.key == pygame.K_DOWN:
        ship.moving_bottom = False


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, booms, bloods):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, booms, bloods)
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人


def update_booms(ai_settings, screen, stats, sb, booms):
    """更新爆炸效果"""
    booms.update()
    for boom in booms.copy():
        if boom.curI == boom.targetI:
            booms.remove(boom)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, booms, bloods):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人

    if len(aliens) == 6 and not ai_settings.hasBoss:
        create_boss(ai_settings, screen, aliens,bloods)
        ai_settings.hasBoss = True
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    # 添加子弹和外星人相撞时的声音
    eat_sound = pygame.mixer.Sound('music/boo.wav')
    if collisions:
        eat_sound.play()
        for alienss in collisions.values():
            for alien1 in alienss:
                alien1.blood -= 1
                if alien1.blood == 0:
                    for blood in bloods.sprites():
                        if blood.alien.blood == 0:
                            bloods.remove_internal(blood)
                    aliens.remove(alien1)
                    boom1 = Boom(alien1, screen, ai_settings)
                    booms.add(boom1)
                else:
                    for blood in bloods.sprites():
                        if blood.alien.blood != 0:
                            blood.resetBloodLength(ai_settings)
            stats.score += ai_settings.alien_points * len(alienss)
            sb.prep_score()
        check_high_score(stats, sb)
    # 如果整群外星人都被消灭了，就提高一个等级
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens, bloods)
        ai_settings.hasBoss = False


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        # 添加发射子弹时的声音
        eat_sound = pygame.mixer.Sound('music/射击声.wav')
        eat_sound.play()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x - 2


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = 3 * alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 20
    aliens.add(alien)


def create_boss(ai_settings, screen, aliens,bloods):
    """创建一个外星boss"""
    boss = Boss(ai_settings, screen)
    boss.x = random.randint(100, 500)
    boss.rect.x = boss.x
    boss.rect.y = 0
    blood=Blood(ai_settings,screen,boss)
    bloods.add(blood)
    aliens.add(boss)


def create_fleet(ai_settings, screen, ship, aliens, bloods):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    # alien = Alien(ai_settings, screen)
    # number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    # number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # # 创建外星人群
    # for row_number in range(number_rows):
    #     for alien_number in range(number_alien_x):
    #         # 创建一个外星人并将其加入当前行
    #         create_alien(ai_settings, screen, aliens, alien_number, row_number)
    for blood in bloods.sprites():
        bloods.remove_internal(blood)

    for i in range(4):
        """创建一个外星人并将其放在当前行"""
        alien = Alien(ai_settings, screen)
        alien.position = "top"
        alien.rect.x = 100 * i + 300
        alien.rect.y = 40
        aliens.add(alien)
        blood1 = Blood(ai_settings, screen, alien)
        bloods.add(blood1)
    for i in range(3):
        """创建一个外星人并将其放在当前行"""
        alien1 = Alien(ai_settings, screen)
        alien1.position = 'left'
        alien1.rect.x = 0
        alien1.y = alien1.rect.y = 50 * i + 90
        aliens.add(alien1)
        alien2 = Alien(ai_settings, screen)
        alien2.position = "right"
        alien2.rect.x = ai_settings.screen_width - alien1.rect.width
        alien2.y = alien2.rect.y = 50 * i + 90
        aliens.add(alien2)
        aliens.add(alien1)
        blood1 = Blood(ai_settings, screen, alien1)
        bloods.add(blood1)
        blood2 = Blood(ai_settings, screen, alien2)
        bloods.add(blood2)


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows - 1


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens, alien)


def change_fleet_direction(ai_settings, aliens, alien):
    """将整个外星人下移，并改变它们的方向"""
    # for alien in aliens.sprites():
    #     if alien.rect.width==40:
    #      alien.rect.y += ai_settings.fleet_drop_speed
    #     else:
    #       alien.rect.y+=2*ai_settings.fleet_drop_speed
    alien.direction = -alien.direction
    # ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, booms, play_button):
    """检查是否有外星人位于屏幕边缘，并更新外星人位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, booms, play_button)
    # 检查是否有外星人抵达屏幕底部
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


def update_bloods(ai_settings, screen, stats, bloods):
    if stats.game_active == True:
        bloods.update()


def ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets, booms, play_button):
    """响应被外星人撞到的飞船"""
    # 添加飞船和外星人相撞时的声音
    eat_sound = pygame.mixer.Sound('music/boo.wav')
    if booms != None:
        boom1 = Boom(ship, screen, ai_setting)
        eat_sound.play()
        booms.add(boom1)
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1
        # 更新计分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        # create_fleet(ai_setting, screen, ship, aliens)
        ship.curC = 1
        ship.isBoom = True
        ship.center_ship()
        # 暂停
        # sleep(0.5)
    else:
        play_button.resSetMsg("Play")
        stats.game_active = False
        pygame.mouse.set_visible(True)
        # 游戏结束将最高分存储到文本中
        with open('maxScore.txt', 'w') as setText:
            setText.write(str(stats.high_score))


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """检查是否有外星人到达了屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, None, play_button)
            break


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, buttes, mouse_x, mouse_y, bloods):
    """在玩家单击Play按钮时开始新游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y) and play_button.msg == "Play":
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        # pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置计分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        buttes.empty()
        ai_settings.hasBoss = False
        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens, bloods)
        ship.center_ship()
        # 读取文本中的内容，设置最高得分
        with open('maxScore.txt', 'r') as readScore:
            stats.high_score = int(readScore.readline())
    else:
        stats.game_active = True


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        # 游戏结束将最高分存储到文本中
        with open('maxScore.txt', 'w') as setText:
            setText.write(str(stats.high_score))
