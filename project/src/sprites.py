"""
============================================================
 🎮 超级小猫 —— sprites.py
 所有游戏对象（精灵）的定义
============================================================
 这里定义了游戏中每一个"会动的东西"：
   Player   — 玩家角色（可爱的橘猫 🐱）
   Platform — 平台（可以站上去的方块）
   Coin     — 金币（旋转闪光 ✨）
   Enemy    — 敌人（紫色小恶魔 👾）
   Flag     — 终点旗帜（🏁）
   Bullet   — 子弹（波动飞行 ~）
   FloatText— 飘字特效（得分提示）

 每个精灵类都继承自 pygame.sprite.Sprite。
============================================================
"""

import pygame
import math
import random
from settings import *


# ============================================================
# 玩家 —— 可爱橘猫 🐱
# ============================================================
class Player(pygame.sprite.Sprite):
    """玩家角色 —— 一只可爱的橘猫"""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self._draw_cat()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 物理
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

        # 状态
        self.facing_right = True
        self.invincible = 0
        self.shoot_cooldown = 0
        self.wants_shoot = False
        self.air_jumps_left = 1   # 空中剩余跳跃次数（1 = 二段跳）
        self.lives = STARTING_LIVES
        self.score = 0

    def _draw_cat(self):
        """绘制橘猫像素画"""
        w, h = PLAYER_WIDTH, PLAYER_HEIGHT
        img = self.image

        # === 耳朵 ===
        # 左耳（三角形）
        pygame.draw.polygon(img, PLAYER_FUR, [(4, 8), (10, 0), (14, 8)])
        pygame.draw.polygon(img, (255, 200, 160), [(7, 6), (11, 2), (13, 6)])  # 内耳
        # 右耳
        pygame.draw.polygon(img, PLAYER_FUR, [(w - 14, 8), (w - 10, 0), (w - 4, 8)])
        pygame.draw.polygon(img, (255, 200, 160), [(w - 13, 6), (w - 11, 2), (w - 7, 6)])

        # === 头 ===
        pygame.draw.ellipse(img, PLAYER_FUR, (2, 4, w - 4, 18))  # 圆脸
        # 脸部白色区域
        pygame.draw.ellipse(img, PLAYER_BELLY, (6, 10, w - 12, 12))

        # === 眼睛 ===
        eye_y = 10
        # 左眼
        pygame.draw.ellipse(img, WHITE, (8, eye_y, 7, 7))
        pygame.draw.ellipse(img, PLAYER_EYE, (10, eye_y + 1, 4, 5))
        pygame.draw.ellipse(img, WHITE, (11, eye_y, 2, 2))  # 高光
        # 右眼
        pygame.draw.ellipse(img, WHITE, (w - 15, eye_y, 7, 7))
        pygame.draw.ellipse(img, PLAYER_EYE, (w - 14, eye_y + 1, 4, 5))
        pygame.draw.ellipse(img, WHITE, (w - 13, eye_y, 2, 2))

        # === 鼻子 ===
        nose_x = w // 2 - 2
        pygame.draw.ellipse(img, (255, 150, 150), (nose_x, 16, 4, 3))

        # === 腮红 ===
        pygame.draw.ellipse(img, PLAYER_CHEEK, (3, 15, 5, 3))
        pygame.draw.ellipse(img, PLAYER_CHEEK, (w - 8, 15, 5, 3))

        # === 胡须 ===
        for ox in [(-5, 8), (-6, 10)]:
            pygame.draw.line(img, PLAYER_WHISKER, (ox[1] + 2, 18), (ox[1] + ox[0], 17), 1)
            pygame.draw.line(img, PLAYER_WHISKER, (ox[1] + 2, 19), (ox[1] + ox[0], 19), 1)
        for ox in [(5, w - 8), (6, w - 10)]:
            pygame.draw.line(img, PLAYER_WHISKER, (ox[1] - 2, 18), (ox[1] + ox[0], 17), 1)
            pygame.draw.line(img, PLAYER_WHISKER, (ox[1] - 2, 19), (ox[1] + ox[0], 19), 1)

        # === 身体 ===
        pygame.draw.ellipse(img, PLAYER_FUR, (4, 20, w - 8, h - 24))
        # 肚皮
        pygame.draw.ellipse(img, PLAYER_BELLY, (8, 24, w - 16, h - 32))

        # === 帽子 ===
        pygame.draw.rect(img, PLAYER_HAT, (2, 0, w - 4, 8))
        pygame.draw.rect(img, PLAYER_HAT, (w // 2 - 6, 0, 14, 4))  # 帽檐

        # === 爪子 ===
        pygame.draw.ellipse(img, PLAYER_FUR, (2, h - 8, 8, 6))
        pygame.draw.ellipse(img, PLAYER_FUR, (w - 10, h - 8, 8, 6))

    def handle_input(self):
        """处理键盘输入：A/D 移动，K 跳跃，J 射击"""
        keys = pygame.key.get_pressed()

        # 左右移动
        self.vel_x = 0
        if keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True

        # 跳跃：K 键（地面跳 或 空中二段跳）
        if keys[pygame.K_k]:
            if self.on_ground:
                self.vel_y = JUMP_POWER
                self.on_ground = False
            elif self.air_jumps_left > 0:
                self.vel_y = JUMP_POWER * 0.85  # 空中跳稍弱
                self.air_jumps_left -= 1

        # 射击：J 键（带冷却）
        self.wants_shoot = False
        if keys[pygame.K_j] and self.shoot_cooldown <= 0:
            self.wants_shoot = True
            self.shoot_cooldown = BULLET_COOLDOWN

    def apply_physics(self):
        """只修改速度，位置由 handle_collisions 统一处理"""
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

    def update(self):
        """每帧调用"""
        self.handle_input()
        self.apply_physics()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1

    def take_damage(self):
        """受伤扣命，返回 True 表示确实受伤了"""
        if self.invincible > 0:
            return False
        self.lives -= 1
        self.invincible = INVINCIBLE_TIME
        return True

    def add_score(self, points):
        self.score += points


# ============================================================
# 平台 —— 砖块纹理 🧱
# ============================================================
class Platform(pygame.sprite.Sprite):
    """平台 —— 砖块纹理，绿色草皮顶部"""

    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, PLATFORM_HEIGHT))
        # 棕色砖块底色
        self.image.fill(PLATFORM_BROWN)
        # 砖块纹理
        for bx in range(0, width, 16):
            brick_color = (
                PLATFORM_BROWN[0] + random.randint(-15, 15),
                PLATFORM_BROWN[1] + random.randint(-10, 10),
                PLATFORM_BROWN[2] + random.randint(-10, 10),
            )
            pygame.draw.rect(self.image, brick_color, (bx, 4, 14, PLATFORM_HEIGHT - 4))
            pygame.draw.rect(self.image, (80, 50, 20), (bx, 4, 14, PLATFORM_HEIGHT - 4), 1)
        # 顶部草皮
        pygame.draw.rect(self.image, PLATFORM_TOP, (0, 0, width, 6))
        # 小草点缀
        for gx in range(4, width, 12):
            grass_h = random.randint(2, 5)
            pygame.draw.rect(self.image, PLATFORM_GRASS, (gx, 2, 3, grass_h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# ============================================================
# 金币 —— 旋转闪亮 ✨
# ============================================================
class Coin(pygame.sprite.Sprite):
    """金币 —— 浮动旋转效果"""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
        self._draw_coin(COIN_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.base_y = y
        self.anim_timer = random.uniform(0, 6.28)
        self.width_scale = COIN_SIZE  # 用于模拟旋转的宽度

    def _draw_coin(self, size):
        """绘制一枚金币"""
        self.image.fill((0, 0, 0, 0))
        cx, cy = size // 2, size // 2
        r = size // 2 - 2
        # 外圈
        pygame.draw.circle(self.image, COIN_BORDER, (cx, cy), r)
        # 内部
        pygame.draw.circle(self.image, COIN_YELLOW, (cx, cy), r - 2)
        # 高光
        pygame.draw.circle(self.image, COIN_SHINE, (cx - 2, cy - 3), max(r // 3, 2))
        # $ 符号
        font = pygame.font.SysFont("Noto Sans CJK SC", max(size // 3, 6), bold=True)
        s = font.render("$", True, COIN_BORDER)
        self.image.blit(s, (cx - s.get_width() // 2, cy - s.get_height() // 2))

    def update(self):
        """上下浮动 + 旋转缩放效果"""
        self.anim_timer += 0.06
        # 上下浮动
        self.rect.y = self.base_y + int(3 * math.sin(self.anim_timer))
        # 水平缩放模拟旋转
        scale = abs(math.cos(self.anim_timer * 0.7))
        self.width_scale = max(COIN_SIZE * 0.4, COIN_SIZE * scale)


# ============================================================
# 敌人 —— 紫色小恶魔 👾
# ============================================================
class Enemy(pygame.sprite.Sprite):
    """敌人 —— 来回巡逻，踩头或子弹消灭"""

    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
        self._draw_demon()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.speed = 2
        self.vel_y = 0

    def _draw_demon(self):
        """绘制紫色小恶魔"""
        w, h = ENEMY_WIDTH, ENEMY_HEIGHT
        img = self.image

        # === 角 ===
        horn_tip_l = [(w // 4, 0), (w // 4 - 3, 10), (w // 4 + 3, 10)]
        horn_tip_r = [(3 * w // 4, 0), (3 * w // 4 - 3, 10), (3 * w // 4 + 3, 10)]
        pygame.draw.polygon(img, ENEMY_HORN, horn_tip_l)
        pygame.draw.polygon(img, ENEMY_HORN, horn_tip_r)

        # === 头 ===
        pygame.draw.ellipse(img, ENEMY_BODY, (2, 6, w - 4, 14))
        pygame.draw.ellipse(img, ENEMY_DARK, (4, 8, w - 8, 10))  # 深色区域

        # === 眼睛 ===
        eye_y = 10
        # 左眼
        pygame.draw.ellipse(img, ENEMY_EYE, (6, eye_y, 8, 8))
        pygame.draw.ellipse(img, ENEMY_PUPIL, (9, eye_y + 1, 4, 5))
        # 右眼
        pygame.draw.ellipse(img, ENEMY_EYE, (w - 14, eye_y, 8, 8))
        pygame.draw.ellipse(img, ENEMY_PUPIL, (w - 13, eye_y + 1, 4, 5))

        # === 嘴（锯齿）===
        mouth_y = 17
        for tx in range(w // 2 - 7, w // 2 + 7, 3):
            pygame.draw.rect(img, WHITE, (tx, mouth_y, 2, 2))
        pygame.draw.line(img, WHITE, (w // 2 - 7, mouth_y), (w // 2 + 7, mouth_y), 1)

        # === 身体 ===
        pygame.draw.ellipse(img, ENEMY_BODY, (4, 20, w - 8, h - 26))
        # 纹理条纹
        for sx in range(4, w - 4, 8):
            pygame.draw.line(img, ENEMY_DARK, (sx, 22), (sx, h - 8), 1)

        # === 脚 ===
        pygame.draw.ellipse(img, ENEMY_DARK, (2, h - 6, 10, 6))
        pygame.draw.ellipse(img, ENEMY_DARK, (w - 12, h - 6, 10, 6))

    def update(self):
        """巡逻移动 + 重力（位置由 handle_collisions 统一处理）"""
        self.rect.x += self.speed
        if self.rect.x <= self.patrol_left:
            self.rect.x = self.patrol_left
            self.speed = abs(self.speed)
        elif self.rect.x >= self.patrol_right:
            self.rect.x = self.patrol_right
            self.speed = -abs(self.speed)
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED


# ============================================================
# 子弹 —— 波动飞行 ~
# ============================================================
class Bullet(pygame.sprite.Sprite):
    """子弹 —— 水平飞行 + 上下正弦波动"""

    def __init__(self, x, y, direction):
        """
        direction: 1 = 向右, -1 = 向左
        """
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT), pygame.SRCALPHA)
        self._draw_bullet()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.base_y = float(y)       # 基准 Y（波动中心）
        self.speed = BULLET_SPEED * direction
        self.osc_timer = 0.0         # 波动计时器

    def _draw_bullet(self):
        """绘制金黄色子弹（带光晕）"""
        w, h = BULLET_WIDTH, BULLET_HEIGHT
        # 光晕
        pygame.draw.ellipse(self.image, BULLET_GLOW, (0, 1, w, h - 2))
        # 主体
        pygame.draw.ellipse(self.image, BULLET_COLOR, (2, 2, w - 4, h - 4))
        # 核心高光
        pygame.draw.ellipse(self.image, WHITE, (w // 2 - 1, 3, 3, 2))

    def update(self):
        """水平飞行 + 正弦波动"""
        self.rect.x += self.speed
        self.osc_timer += BULLET_OSC_FREQ
        self.rect.y = int(self.base_y + BULLET_OSC_AMP * math.sin(self.osc_timer))
        # 超出世界边界则销毁（世界坐标，需覆盖最宽关卡）
        if self.rect.right < -200 or self.rect.left > 6000:
            self.kill()


# ============================================================
# 敌人子弹 —— 敌人和 Boss 发射的弹幕 🔴
# ============================================================
class EnemyBullet(pygame.sprite.Sprite):
    """敌人子弹 —— 直线飞行，碰到玩家造成伤害"""

    def __init__(self, x, y, vx, vy=0):
        super().__init__()
        self.image = pygame.Surface((ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT), pygame.SRCALPHA)
        self._draw()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vel_x = vx
        self.vel_y = vy

    def _draw(self):
        w, h = ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT
        # 光晕
        pygame.draw.circle(self.image, ENEMY_BULLET_GLOW, (w // 2, h // 2), w // 2)
        # 主体
        pygame.draw.circle(self.image, ENEMY_BULLET_COLOR, (w // 2, h // 2), w // 2 - 2)
        # 核心
        pygame.draw.circle(self.image, WHITE, (w // 2 - 1, h // 2 - 1), 2)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # 超出世界边界则销毁（世界坐标，需覆盖最宽关卡）
        if (self.rect.right < -200 or self.rect.left > 6000 or
                self.rect.bottom < -100 or self.rect.top > SCREEN_HEIGHT + 200):
            self.kill()


# ============================================================
# 飞行敌人 —— 红色蝙蝠 🦇
# ============================================================
class FlyingEnemy(pygame.sprite.Sprite):
    """飞行敌人 —— 垂直上下巡逻，只能被子弹消灭，碰到玩家受伤"""

    def __init__(self, x, y, patrol_top, patrol_bottom):
        super().__init__()
        self.image = pygame.Surface((FLYING_ENEMY_WIDTH, FLYING_ENEMY_HEIGHT), pygame.SRCALPHA)
        self._draw_bat()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.base_x = x
        self.patrol_top = patrol_top
        self.patrol_bottom = patrol_bottom
        self.speed_x = FLYING_ENEMY_SPEED * 0.5  # 水平飘移
        self.speed_y = FLYING_ENEMY_SPEED
        self.anim_timer = random.uniform(0, 6.28)

    def _draw_bat(self):
        w, h = FLYING_ENEMY_WIDTH, FLYING_ENEMY_HEIGHT
        img = self.image

        # 翅膀（左右展开）
        wing_pts_l = [(w // 2, h // 2 - 4), (2, h // 2 - 10), (4, h // 2), (2, h // 2 + 10)]
        wing_pts_r = [(w // 2, h // 2 - 4), (w - 2, h // 2 - 10), (w - 4, h // 2), (w - 2, h // 2 + 10)]
        pygame.draw.polygon(img, FLYING_WING, wing_pts_l)
        pygame.draw.polygon(img, FLYING_WING, wing_pts_r)

        # 身体
        pygame.draw.ellipse(img, FLYING_BODY, (w // 4, h // 4, w // 2, h // 2))

        # 眼睛
        eye_y = h // 2 - 3
        pygame.draw.ellipse(img, FLYING_EYE, (w // 2 - 4, eye_y - 4, 4, 5))
        pygame.draw.ellipse(img, FLYING_EYE, (w // 2 + 1, eye_y - 4, 4, 5))
        pygame.draw.ellipse(img, BLACK, (w // 2 - 3, eye_y - 3, 2, 3))
        pygame.draw.ellipse(img, BLACK, (w // 2 + 2, eye_y - 3, 2, 3))

        # 尖牙
        pygame.draw.polygon(img, WHITE, [(w // 2 - 2, h // 2 + 3), (w // 2, h // 2 + 8), (w // 2 + 2, h // 2 + 3)])

    def update(self):
        """垂直巡逻 + 轻微水平飘动"""
        self.rect.y += self.speed_y
        if self.rect.top <= self.patrol_top:
            self.speed_y = abs(self.speed_y)
        elif self.rect.bottom >= self.patrol_bottom:
            self.speed_y = -abs(self.speed_y)

        # 轻微水平摆动
        self.anim_timer += 0.04
        self.rect.x = self.base_x + int(20 * math.sin(self.anim_timer))


# ============================================================
# 射击敌人 —— 绿色炮台 👾
# ============================================================
class ShootingEnemy(pygame.sprite.Sprite):
    """射击敌人 —— 站在平台上，定期向玩家方向发射子弹"""

    def __init__(self, x, y, shoot_interval=SHOOTING_ENEMY_COOLDOWN):
        super().__init__()
        self.image = pygame.Surface((SHOOTING_ENEMY_WIDTH, SHOOTING_ENEMY_HEIGHT), pygame.SRCALPHA)
        self._draw_turret()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shoot_timer = random.randint(0, shoot_interval)  # 随机初始冷却
        self.shoot_interval = shoot_interval
        self.should_shoot = False
        self.shoot_direction = -1  # 默认向左

    def _draw_turret(self):
        w, h = SHOOTING_ENEMY_WIDTH, SHOOTING_ENEMY_HEIGHT
        img = self.image

        # 底座
        pygame.draw.rect(img, SHOOTING_BARREL, (2, h // 2, w - 4, h // 2))
        pygame.draw.rect(img, (20, 70, 20), (2, h // 2, w - 4, h // 2), 2)

        # 炮管
        pygame.draw.rect(img, SHOOTING_BARREL, (w // 2 - 3, 0, 6, h // 2 + 4))
        pygame.draw.rect(img, (20, 50, 20), (w // 2 - 3, 0, 6, h // 2 + 4), 1)

        # 头部
        pygame.draw.ellipse(img, SHOOTING_BODY, (w // 4, h // 4, w // 2, h // 2))

        # 眼睛（怒视状）
        eye_y = h // 3 + 4
        pygame.draw.ellipse(img, SHOOTING_EYE, (w // 4 + 2, eye_y, 7, 7))
        pygame.draw.ellipse(img, SHOOTING_EYE, (w // 2 + 2, eye_y, 7, 7))
        # 瞳孔（红色）
        pygame.draw.ellipse(img, RED, (w // 4 + 4, eye_y + 1, 4, 5))
        pygame.draw.ellipse(img, RED, (w // 2 + 4, eye_y + 1, 4, 5))

    def update(self):
        """倒计时射击冷却"""
        if self.shoot_timer > 0:
            self.shoot_timer -= 1

    def ready_to_shoot(self):
        """是否准备好射击"""
        return self.shoot_timer <= 0

    def shoot(self):
        """重置射击冷却"""
        self.shoot_timer = self.shoot_interval


# ============================================================
# Boss —— 暗黑魔王 👑
# ============================================================
class Boss(pygame.sprite.Sprite):
    """最终 Boss —— 大魔王，拥有多种攻击模式和生命条"""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BOSS_WIDTH, BOSS_HEIGHT), pygame.SRCALPHA)
        self._draw_boss()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 生命
        self.max_health = BOSS_HEALTH
        self.health = BOSS_HEALTH

        # 移动
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.speed = BOSS_SPEED
        self.move_timer = 0
        self.move_target = x
        self.arena_left = x - 300
        self.arena_right = x + 500

        # 攻击
        self.attack_cooldown = BOSS_ATTACK_COOLDOWN
        self.attack_timer = 60  # 首次攻击稍等
        self.attack_pattern = 0  # 0=追踪弹, 1=扇形散射, 2=冲刺
        self.phase = 1           # 1=普通, 2=愤怒
        self.charging = False
        self.charge_target = 0
        self.charge_speed_x = 0

        # 无敌（受伤闪烁）
        self.invincible_timer = 0

    def _draw_boss(self):
        w, h = BOSS_WIDTH, BOSS_HEIGHT
        img = self.image

        # === 王冠 ===
        crown_pts = [(w // 2 - 18, 0), (w // 2 - 22, 14), (w // 2 - 8, 6),
                     (w // 2, 20), (w // 2 + 8, 6), (w // 2 + 22, 14), (w // 2 + 18, 0)]
        pygame.draw.polygon(img, BOSS_CROWN, crown_pts)
        # 宝石
        pygame.draw.ellipse(img, BOSS_CROWN_GEM, (w // 2 - 4, 6, 8, 8))

        # === 角 ===
        pygame.draw.polygon(img, BOSS_HORN, [(w // 2 - 22, 20), (w // 2 - 28, -6), (w // 2 - 14, 18)])
        pygame.draw.polygon(img, BOSS_HORN, [(w // 2 + 22, 20), (w // 2 + 28, -6), (w // 2 + 14, 18)])

        # === 头 ===
        pygame.draw.ellipse(img, BOSS_BODY, (8, 14, w - 16, 32))
        pygame.draw.ellipse(img, BOSS_DARK, (12, 18, w - 24, 24))

        # === 眼睛（发红光的邪恶眼）===
        eye_y = 22
        # 左眼
        pygame.draw.ellipse(img, BOSS_EYE, (16, eye_y, 14, 12))
        pygame.draw.ellipse(img, WHITE, (19, eye_y + 1, 5, 4))  # 高光
        # 右眼
        pygame.draw.ellipse(img, BOSS_EYE, (w - 30, eye_y, 14, 12))
        pygame.draw.ellipse(img, WHITE, (w - 24, eye_y + 1, 5, 4))

        # === 嘴（锯齿状）===
        mouth_y = 38
        for tx in range(w // 2 - 10, w // 2 + 10, 4):
            pygame.draw.rect(img, WHITE, (tx, mouth_y, 3, 3))
        pygame.draw.line(img, WHITE, (w // 2 - 10, mouth_y + 4), (w // 2 + 10, mouth_y + 4), 2)

        # === 身体 ===
        pygame.draw.ellipse(img, BOSS_BODY, (4, 42, w - 8, h - 52))
        pygame.draw.ellipse(img, BOSS_DARK, (10, 46, w - 20, h - 60))

        # === 铠甲条纹 ===
        for i in range(3):
            sy = 50 + i * 8
            pygame.draw.line(img, (80, 10, 120), (12, sy), (w - 12, sy), 2)

        # === 爪子 ===
        pygame.draw.ellipse(img, BOSS_DARK, (0, h - 14, 14, 12))
        pygame.draw.ellipse(img, BOSS_DARK, (w - 14, h - 14, 14, 12))

    def update(self):
        """Boss AI：根据阶段执行不同行为"""
        # 无敌计时
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # 检查是否进入愤怒阶段
        if self.health <= self.max_health * BOSS_ENRAGE_THRESHOLD and self.phase == 1:
            self.phase = 2
            self.speed = BOSS_SPEED * 1.5
            self.attack_cooldown = BOSS_SHOOT_COOLDOWN_FAST

        # 冲刺模式中
        if self.charging:
            self.rect.x += self.charge_speed_x
            # 碰到竞技场边界或转向
            if self.rect.left <= self.arena_left or self.rect.right >= self.arena_right:
                self.charge_speed_x *= -1
                self.charging = False
                self.attack_timer = self.attack_cooldown
            return

        # 攻击计时
        if self.attack_timer > 0:
            self.attack_timer -= 1

        # 移动AI：在竞技场内左右巡逻
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.move_timer = random.randint(60, 150)
            self.move_target = random.randint(
                max(self.arena_left, self.rect.x - 200),
                min(self.arena_right, self.rect.x + 200)
            )

        if self.rect.centerx < self.move_target - 10:
            self.vel_x = self.speed
        elif self.rect.centerx > self.move_target + 10:
            self.vel_x = -self.speed
        else:
            self.vel_x = 0

        # 重力
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # 限制在竞技场内
        if self.rect.left < self.arena_left:
            self.rect.left = self.arena_left
        if self.rect.right > self.arena_right:
            self.rect.right = self.arena_right

    def take_damage(self):
        """受到伤害，返回 True 表示被击杀了"""
        if self.invincible_timer > 0:
            return False
        self.health -= 1
        self.invincible_timer = 8  # 短暂无敌
        return self.health <= 0

    def get_attack_data(self, player_x, player_y):
        """
        根据当前阶段和攻击模式，返回本次攻击的子弹数据列表。
        返回格式: [(x, y, vx, vy), ...]
        如果返回空列表，表示本次不攻击或近战冲刺。
        """
        if self.attack_timer > 0 or self.charging:
            return []

        # 切换攻击模式
        self.attack_pattern = (self.attack_pattern + 1) % 3
        self.attack_timer = self.attack_cooldown
        bullets = []

        cx, cy = self.rect.centerx, self.rect.centery

        if self.attack_pattern == 0:
            # 追踪弹：向玩家方向发射1-2颗子弹
            dx = player_x - cx
            dy = player_y - cy
            dist = max(1, math.sqrt(dx * dx + dy * dy))
            speed = BOSS_BULLET_SPEED
            vx = dx / dist * speed
            vy = dy / dist * speed
            bullets.append((cx, cy, vx, vy))
            if self.phase == 2:
                # 愤怒模式：散一点角度
                angle = math.atan2(dy, dx) + 0.3
                bullets.append((cx, cy, math.cos(angle) * speed, math.sin(angle) * speed))
                angle = math.atan2(dy, dx) - 0.3
                bullets.append((cx, cy, math.cos(angle) * speed, math.sin(angle) * speed))

        elif self.attack_pattern == 1:
            # 扇形散射
            dx = player_x - cx
            dy = player_y - cy
            base_angle = math.atan2(dy, dx)
            spread = BOSS_BULLET_SPREAD
            for i in range(spread):
                angle = base_angle - 0.4 + (0.8 / max(1, spread - 1)) * i
                bullets.append((cx, cy,
                               math.cos(angle) * BOSS_BULLET_SPEED,
                               math.sin(angle) * BOSS_BULLET_SPEED))

        elif self.attack_pattern == 2:
            # 冲刺：Boss 冲向玩家
            self.charging = True
            if player_x < cx:
                self.charge_speed_x = -BOSS_CHARGE_SPEED
            else:
                self.charge_speed_x = BOSS_CHARGE_SPEED

        return bullets

    def is_charging(self):
        return self.charging


# ============================================================
# 旗帜 —— 终点 🏁
# ============================================================
class Flag(pygame.sprite.Sprite):
    """终点旗帜"""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((FLAG_WIDTH, FLAG_HEIGHT), pygame.SRCALPHA)
        self._draw_flag()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _draw_flag(self):
        """绘制带星星的旗帜"""
        w, h = FLAG_WIDTH, FLAG_HEIGHT
        # 旗杆（金属光泽）
        pole_w = 4
        for i in range(pole_w):
            shade = FLAG_POLE[0] - i * 20
            pygame.draw.rect(self.image, (max(shade, 50), max(shade, 50), max(shade, 50)),
                             (w // 2 - pole_w // 2 + i, 0, 1, h))
        # 杆顶圆球
        pygame.draw.circle(self.image, (255, 255, 100), (w // 2, 6), 4)
        # 三角红旗
        flag_pts = [(w // 2, 10), (w - 2, 28), (w // 2, 46)]
        pygame.draw.polygon(self.image, FLAG_RED, flag_pts)
        # 旗上小星星
        pygame.draw.circle(self.image, FLAG_STAR, (w // 2 + 4, 24), 3)


# ============================================================
# 飘字特效
# ============================================================
class FloatText(pygame.sprite.Sprite):
    """得分飘字"""

    def __init__(self, x, y, text, color=YELLOW):
        super().__init__()
        self.font = pygame.font.SysFont("Noto Sans CJK SC", 20, bold=True)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.life = 30
        self.vel_y = -2

    def update(self):
        self.rect.y += self.vel_y
        self.life -= 1
        if self.life <= 0:
            self.kill()
