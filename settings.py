class Settings():
    """储存《外星人入侵》的所有设置"""
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕的设置
        self.screen_width=900
        self.screen_height=600
        self.bg_color=(60,63,65)
        #飞船的设置
        self.ship_speed_factor=3
        self.ship_limit=3
        #子弹的设置
        self.bullet_speed_factor=3
        self.bullet_width=3
        self.bullet_height=12
        self.bullet_color=100,216,238
        self.bullets_allowed=6
        #外星人设置
        self.alien_speed_factor=1
        self.fleet_drop_speed=5
        self.alien_blood=2
        self.boss_blood=5
        #fleet_direction为1表示向右移动，为-1表示向左移
        self.fleet_direction=0.8
        #以什么样的速度加快游戏节奏
        self.speedup_scale=1.1
        #外星人点数的提高速度
        self.score_scale=1.5
        self.initialize_dynamic_settings()
        #这组外星人是否已经出现过外星人
        self.hasBoss=False
        #血量条的设置
        self.blood_width=36
        self.blood_height=3
        self.blood_color1 = 202, 34, 41
        self.blood_color2 = 59, 176, 255
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1

        #fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction=1
        #计分
        self.alien_points=50
    def increase_speed(self):

        """提供速度设置和外星人点数"""
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale
        self.alien_pofints=int(self.alien_points*self.score_scale)
