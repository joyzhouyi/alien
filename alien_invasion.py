from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import pygame, sys

def run_game():

    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    # 添加背景音乐
    pygame.mixer.music.load('music/backgroundMusic.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    # eat_sound = pygame.mixer.Sound('music/bgm.mp3')
    # eat_sound.play()
    icon = pygame.image.load("images/icon1.png")
    pygame.display.set_icon(icon)
    # # 添加吃到食物的音效
    # eat_sound = pygame.mixer.Sound('music/yeah.wav')
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建一艘飞船创建一个用于存储子弹的编组
    ship = Ship(ai_settings,screen )
    bullets = Group()
    aliens = Group()
    booms=Group()
    bloods=Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens,bloods)
    fClock = pygame.time.Clock()
    fps = 80
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    continue_button = Button(ai_settings, screen, "Continue")
    # 创建存储游戏统计信息的实例，并创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats,sb, play_button, ship, aliens, bullets,bloods)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,booms,bloods)
            gf.update_aliens(ai_settings,  screen,stats,sb, ship, aliens, bullets,booms,play_button )
            gf.update_booms(ai_settings,screen,stats,sb,booms)
            gf.update_bloods(ai_settings,screen,stats,bloods)
            print(len(bloods))
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button,booms,bloods)
        fClock.tick(fps)


# 以主程序形式运行
if __name__ == '__main__':
    run_game()
