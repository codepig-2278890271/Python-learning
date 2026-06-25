"""
============================================================
 🎮 超级小猫 —— main.py
 游戏入口 & 主循环
============================================================
 这个文件是整个游戏的"心脏"：
   - 初始化 pygame
   - 管理游戏状态机（菜单 → 游戏中 → 死亡/通关）
   - 每一帧：处理输入 → 更新精灵 → 碰撞检测 → 绘制画面

 运行方法：
   python3 main.py

 游戏状态机：
   STATE_MENU     → 开始菜单
   STATE_PLAYING  → 游戏中
   STATE_PAUSED   → 暂停（ESC 切换）
   STATE_GAMEOVER → 死亡画面
   STATE_WIN      → 通关画面

 操作说明：
   A / D  → 左右移动
   K      → 跳跃
   J      → 发射子弹
   ESC    → 暂停 / 继续
============================================================
"""

import pygame
import sys
import os
import logging
from datetime import datetime
from settings import *
from sprites import Player, Platform, Coin, Enemy, Flag, FloatText, Bullet, \
    FlyingEnemy, ShootingEnemy, Boss, EnemyBullet
from level import get_level
from ui import UI

# ============================================================
# 日志系统 —— 记录游戏运行信息到 log/ 目录
# ============================================================
def _setup_logging():
    """初始化日志：同时输出到文件和终端"""
    # 确定日志目录（兼容脚本运行和 PyInstaller 编译后的 exe）
    if getattr(sys, 'frozen', False):
        # PyInstaller 编译的 exe：日志放在 build/log/ 下
        base_dir = os.path.dirname(os.path.dirname(sys.executable))
    else:
        # 脚本运行：日志放在项目根目录的 log/ 下
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)  # src/ 的上一级

    log_dir = os.path.join(base_dir, "log")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("SuperCat")

logger = _setup_logging()


class Game:
    """游戏主类 —— 管理整个游戏的生命周期"""

    def __init__(self):
        """初始化 pygame 和游戏各组件"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.ui = UI()
        logger.info(f"游戏初始化完成 — 窗口 {SCREEN_WIDTH}x{SCREEN_HEIGHT}, FPS={FPS}")

        # 状态机
        self.STATE_MENU = "menu"
        self.STATE_PLAYING = "playing"
        self.STATE_PAUSED = "paused"
        self.STATE_GAMEOVER = "gameover"
        self.STATE_WIN = "win"
        self.state = self.STATE_MENU

        # 精灵组（在 build_level 中填充）
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.flying_enemies = pygame.sprite.Group()
        self.shooting_enemies = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        self.float_texts = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()  # 只含 Boss

        # 关卡追踪
        self.current_level = 1

        # 玩家（在 build_level 中创建）
        self.player = None
        self.level_data = None
        self.level_name = ""
        self.camera_x = 0  # 摄像机偏移

    # ============================================================
    # 关卡构建
    # ============================================================
    def build_level(self, level_num=1):
        """根据关卡数据构建精灵组"""
        # 清空所有精灵
        self.all_sprites.empty()
        self.platforms.empty()
        self.coins.empty()
        self.enemies.empty()
        self.flying_enemies.empty()
        self.shooting_enemies.empty()
        self.flags.empty()
        self.float_texts.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.boss_group.empty()

        # 获取关卡数据
        self.level_data = get_level(level_num)
        self.level_name = self.level_data["name"]
        self.current_level = level_num
        boss_data = self.level_data.get("boss")
        logger.info(f"加载关卡{level_num}: {self.level_name} (平台{len(self.level_data['platforms'])}个, "
                    f"金币{len(self.level_data['coins'])}个, 敌人{len(self.level_data['enemies'])}个, "
                    f"飞行{len(self.level_data.get('flying_enemies', []))}个, "
                    f"炮台{len(self.level_data.get('shooting_enemies', []))}个"
                    f"{', Boss关!' if boss_data else ''})")

        # 创建平台
        for x, y, width in self.level_data["platforms"]:
            p = Platform(x, y, width)
            self.platforms.add(p)
            self.all_sprites.add(p)

        # 创建金币
        for x, y in self.level_data["coins"]:
            c = Coin(x, y)
            self.coins.add(c)
            self.all_sprites.add(c)

        # 创建巡逻敌人
        for x, y, patrol_l, patrol_r in self.level_data["enemies"]:
            e = Enemy(x, y, patrol_l, patrol_r)
            self.enemies.add(e)
            self.all_sprites.add(e)

        # 创建飞行敌人（蝙蝠）
        for x, y, patrol_top, patrol_bottom in self.level_data.get("flying_enemies", []):
            fe = FlyingEnemy(x, y, patrol_top, patrol_bottom)
            self.flying_enemies.add(fe)
            self.all_sprites.add(fe)

        # 创建射击敌人（炮台）
        for x, y in self.level_data.get("shooting_enemies", []):
            se = ShootingEnemy(x, y)
            self.shooting_enemies.add(se)
            self.all_sprites.add(se)

        # 创建 Boss
        if boss_data:
            bx, by = boss_data
            boss = Boss(bx, by)
            self.boss_group.add(boss)
            self.all_sprites.add(boss)

        # 创建旗帜（非 Boss 关才有）
        flag_data = self.level_data.get("flag")
        if flag_data:
            fx, fy = flag_data
            flag = Flag(fx, fy)
            self.flags.add(flag)
            self.all_sprites.add(flag)

        # 创建玩家
        px, py = self.level_data["player_start"]
        self.player = Player(px, py)
        self.all_sprites.add(self.player)

        # 重置摄像机
        self.camera_x = 0

    # ============================================================
    # 重置游戏
    # ============================================================
    def reset_game(self):
        """从头开始游戏"""
        logger.info("游戏开始！")
        self.current_level = 1
        self.build_level(1)
        self.state = self.STATE_PLAYING

    def next_level(self):
        """进入下一关"""
        next_lv = self.current_level + 1
        if next_lv > TOTAL_LEVELS:
            # 已经通关所有关卡（正常情况不会到这儿，旗帜/Boss已触发WIN）
            self.state = self.STATE_WIN
            return
        logger.info(f"进入第 {next_lv} 关！")
        self.build_level(next_lv)
        self.state = self.STATE_PLAYING

    # ============================================================
    # 碰撞处理
    # ============================================================
    def handle_collisions(self):
        """处理所有碰撞：平台、金币、敌人、旗帜、Boss"""

        # ---- 1. 水平碰撞（平台）----
        self.player.rect.x += self.player.vel_x
        hit_platforms = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for plat in hit_platforms:
            if self.player.vel_x > 0:   # 向右走，碰到左边
                self.player.rect.right = plat.rect.left
            elif self.player.vel_x < 0: # 向左走，碰到右边
                self.player.rect.left = plat.rect.right
            self.player.vel_x = 0

        # ---- 2. 垂直碰撞（平台）----
        self.player.rect.y += self.player.vel_y
        hit_platforms = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for plat in hit_platforms:
            if self.player.vel_y > 0:   # 下落中，脚踩平台
                self.player.rect.bottom = plat.rect.top
                self.player.vel_y = 0
                self.player.on_ground = True
                self.player.air_jumps_left = 1  # 落地重置二段跳
            elif self.player.vel_y < 0: # 上升中，头顶撞平台
                self.player.rect.top = plat.rect.bottom
                self.player.vel_y = 0

        # 用碰撞结果判断是否在地面上（不重新检测，防止边界问题）
        if not hit_platforms and self.player.vel_y > 0:
            self.player.on_ground = False

        # ---- 3. 敌人与平台碰撞（让敌人也站在平台上）----
        for enemy in self.enemies:
            enemy.rect.y += enemy.vel_y
            hit = pygame.sprite.spritecollide(enemy, self.platforms, False)
            if hit and enemy.vel_y > 0:
                enemy.rect.bottom = hit[0].rect.top
                enemy.vel_y = 0

        # ---- 4. 金币收集 ----
        collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in collected_coins:
            self.player.add_score(COIN_SCORE)
            ft = FloatText(coin.rect.centerx, coin.rect.top,
                           f"+{COIN_SCORE}", YELLOW)
            self.float_texts.add(ft)
            self.all_sprites.add(ft)

        # ---- 5. 巡逻敌人碰撞 ----
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hit_enemies:
            if self.player.vel_y > 0 and self.player.rect.bottom <= enemy.rect.top + 15:
                enemy.kill()
                self.player.vel_y = JUMP_POWER * 0.6
                self.player.add_score(ENEMY_KILL_SCORE)
                ft = FloatText(enemy.rect.centerx, enemy.rect.top,
                               f"+{ENEMY_KILL_SCORE}", GREEN)
                self.float_texts.add(ft)
                self.all_sprites.add(ft)
            else:
                self._damage_player()

        # ---- 6. 飞行敌人碰撞（不能踩，只能射）----
        hit_flying = pygame.sprite.spritecollide(self.player, self.flying_enemies, False)
        for fe in hit_flying:
            self._damage_player()

        # ---- 7. 射击敌人碰撞（可以踩，也可以射）----
        hit_shooting = pygame.sprite.spritecollide(self.player, self.shooting_enemies, False)
        for se in hit_shooting:
            if self.player.vel_y > 0 and self.player.rect.bottom <= se.rect.top + 15:
                se.kill()
                self.player.vel_y = JUMP_POWER * 0.6
                self.player.add_score(ENEMY_KILL_SCORE)
                ft = FloatText(se.rect.centerx, se.rect.top,
                               f"+{ENEMY_KILL_SCORE}", GREEN)
                self.float_texts.add(ft)
                self.all_sprites.add(ft)
            else:
                self._damage_player()

        # ---- 8. 敌人子弹碰撞 ----
        hit_eb = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hit_eb:
            self._damage_player()

        # ---- 9. Boss 碰撞 ----
        for boss in self.boss_group:
            if self.player.rect.colliderect(boss.rect):
                # 踩头 Boss 也会造成伤害
                if self.player.vel_y > 0 and self.player.rect.bottom <= boss.rect.top + 20:
                    if boss.take_damage():
                        self._defeat_boss()
                    self.player.vel_y = JUMP_POWER * 0.7
                    ft = FloatText(boss.rect.centerx, boss.rect.top, "-1", RED)
                    self.float_texts.add(ft)
                    self.all_sprites.add(ft)
                else:
                    self._damage_player()

        # ---- 10. 旗帜碰撞（通关 → 下一关或通关画面）----
        if pygame.sprite.spritecollide(self.player, self.flags, False):
            if self.current_level < TOTAL_LEVELS:
                logger.info(f"🏁 第{self.current_level}关完成！进入下一关")
                self.next_level()
            else:
                logger.info(f"🎉 全部通关！最终得分: {self.player.score}")
                self.state = self.STATE_WIN

    def _damage_player(self):
        """玩家受到伤害的统一处理"""
        if self.player.take_damage():
            logger.info(f"玩家受伤！剩余生命: {self.player.lives}")
            if self.player.lives <= 0:
                logger.info(f"游戏结束 — 最终得分: {self.player.score}")
                self.state = self.STATE_GAMEOVER
            else:
                self.respawn_player()

    def _defeat_boss(self):
        """击败 Boss 后的处理"""
        logger.info(f"👑 Boss 被击败！最终得分: {self.player.score}")
        self.player.add_score(BOSS_KILL_SCORE)
        # 消灭 Boss（从所有组中移除）
        for boss in self.boss_group:
            boss.kill()
        ft = FloatText(SCREEN_WIDTH // 2 + self.camera_x, SCREEN_HEIGHT // 2,
                       f"+{BOSS_KILL_SCORE} BOSS击杀！", YELLOW)
        self.float_texts.add(ft)
        self.all_sprites.add(ft)
        self.state = self.STATE_WIN

    # ============================================================
    # 玩家重生
    # ============================================================
    def respawn_player(self):
        """玩家受伤后重生到关卡起点"""
        px, py = self.level_data["player_start"]
        self.player.rect.x = px
        self.player.rect.y = py
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.player.invincible = INVINCIBLE_TIME
        self.camera_x = 0

    # ============================================================
    # 更新摄像机
    # ============================================================
    def update_camera(self):
        """让摄像机跟随玩家向右滚动"""
        # 玩家在屏幕右半部分时，摄像机向右移动
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 3
        # 摄像机不能向左移（不允许倒退）
        if target_x > self.camera_x:
            # 平滑跟随
            self.camera_x += (target_x - self.camera_x) * 0.1
        # 摄像机不能小于0（不能看到关卡外）
        if self.camera_x < 0:
            self.camera_x = 0

    # ============================================================
    # 处理事件
    # ============================================================
    def handle_events(self):
        """处理键盘、鼠标和窗口事件"""
        for event in pygame.event.get():
            # 关闭窗口
            if event.type == pygame.QUIT:
                self.running = False

            # 按键
            if event.type == pygame.KEYDOWN:
                # 菜单状态：任意键开始（Q 退出）
                if self.state == self.STATE_MENU:
                    if event.key == pygame.K_q:
                        self.running = False
                    else:
                        self.reset_game()

                # 游戏中 / 暂停中：ESC 切换暂停
                elif self.state in (self.STATE_PLAYING, self.STATE_PAUSED):
                    if event.key == pygame.K_ESCAPE:
                        if self.state == self.STATE_PLAYING:
                            self.state = self.STATE_PAUSED
                            pygame.mouse.set_visible(True)
                            logger.info("游戏暂停")
                        else:
                            self.state = self.STATE_PLAYING
                            pygame.mouse.set_visible(False)
                            logger.info("游戏继续")

                # 死亡/通关：R 重来，Q 退出
                elif self.state in (self.STATE_GAMEOVER, self.STATE_WIN):
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        self.running = False

            # 鼠标点击（暂停菜单按钮）
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == self.STATE_PAUSED:
                self._handle_pause_click(event.pos)

    def _handle_pause_click(self, mouse_pos):
        """处理暂停菜单的鼠标点击"""
        buttons = self.ui.get_pause_buttons()
        for name, rect in buttons:
            if rect.collidepoint(mouse_pos):
                if name == "resume":
                    self.state = self.STATE_PLAYING
                    pygame.mouse.set_visible(False)
                elif name == "quit":
                    self.running = False

    # ============================================================
    # 更新（每一帧）
    # ============================================================
    def update(self):
        """更新游戏中所有对象的状态（仅在 PLAYING 状态）"""
        if self.state != self.STATE_PLAYING:
            return

        # 更新精灵
        self.all_sprites.update()

        # 射击敌人AI：定期向玩家发射子弹
        self._update_shooting_enemies()

        # Boss AI：攻击模式
        self._update_boss_attacks()

        # Boss 平台碰撞
        self._update_boss_platform_collision()

        # 子弹生成：玩家按下 J 时发射
        if self.player.wants_shoot:
            self._spawn_bullet()

        # 子弹已在 all_sprites.update() 中更新过，不要重复调用
        # 只处理碰撞

        # 子弹与敌人碰撞（包括所有敌人类型和Boss）
        self._handle_bullet_enemy_collisions()

        # 碰撞检测
        self.handle_collisions()

        # 更新摄像机
        self.update_camera()

        # 检查玩家是否掉出屏幕
        if self.player.rect.top > SCREEN_HEIGHT + 100:
            logger.info(f"玩家掉落！剩余生命: {self.player.lives - 1}")
            self._damage_player()

    def _spawn_bullet(self):
        """在玩家位置生成一颗子弹"""
        direction = 1 if self.player.facing_right else -1
        bullet_x = self.player.rect.centerx + (15 * direction)
        bullet_y = self.player.rect.centery - 5
        bullet = Bullet(bullet_x, bullet_y, direction)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def _update_shooting_enemies(self):
        """射击敌人AI：定期向玩家方向发射子弹"""
        for se in self.shooting_enemies:
            if se.ready_to_shoot():
                se.shoot()
                # 计算朝向玩家方向
                dx = self.player.rect.centerx - se.rect.centerx
                dy = self.player.rect.centery - se.rect.centery
                dist = max(1, (dx * dx + dy * dy) ** 0.5)
                vx = dx / dist * ENEMY_BULLET_SPEED
                vy = dy / dist * ENEMY_BULLET_SPEED
                bullet = EnemyBullet(se.rect.centerx, se.rect.centery, vx, vy)
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)

    def _update_boss_attacks(self):
        """Boss AI：执行攻击模式"""
        for boss in self.boss_group:
            if boss.health <= 0:
                continue
            attack_bullets = boss.get_attack_data(
                self.player.rect.centerx, self.player.rect.centery)
            if attack_bullets:
                for bx, by, vx, vy in attack_bullets:
                    bullet = EnemyBullet(bx, by, vx, vy)
                    self.enemy_bullets.add(bullet)
                    self.all_sprites.add(bullet)

    def _update_boss_platform_collision(self):
        """Boss 站在平台上（受重力影响）"""
        for boss in self.boss_group:
            if boss.health <= 0:
                continue
            hit = pygame.sprite.spritecollide(boss, self.platforms, False)
            if hit and boss.vel_y > 0:
                boss.rect.bottom = hit[0].rect.top
                boss.vel_y = 0
                boss.on_ground = True

    def _handle_bullet_enemy_collisions(self):
        """子弹击中敌人：消灭敌人 + 加分 + 飘字"""
        for bullet in self.bullets:
            # 巡逻敌人
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, True)
            if hit_enemies:
                bullet.kill()
                for enemy in hit_enemies:
                    self.player.add_score(ENEMY_KILL_SCORE)
                    ft = FloatText(enemy.rect.centerx, enemy.rect.top,
                                   f"+{ENEMY_KILL_SCORE}", GREEN)
                    self.float_texts.add(ft)
                    self.all_sprites.add(ft)
                continue

            # 飞行敌人
            hit_flying = pygame.sprite.spritecollide(bullet, self.flying_enemies, True)
            if hit_flying:
                bullet.kill()
                for fe in hit_flying:
                    self.player.add_score(ENEMY_KILL_SCORE)
                    ft = FloatText(fe.rect.centerx, fe.rect.top,
                                   f"+{ENEMY_KILL_SCORE}", GREEN)
                    self.float_texts.add(ft)
                    self.all_sprites.add(ft)
                continue

            # 射击敌人
            hit_shooting = pygame.sprite.spritecollide(bullet, self.shooting_enemies, True)
            if hit_shooting:
                bullet.kill()
                for se in hit_shooting:
                    self.player.add_score(ENEMY_KILL_SCORE)
                    ft = FloatText(se.rect.centerx, se.rect.top,
                                   f"+{ENEMY_KILL_SCORE}", GREEN)
                    self.float_texts.add(ft)
                    self.all_sprites.add(ft)
                continue

            # Boss（子弹击中 Boss）
            hit_boss = pygame.sprite.spritecollide(bullet, self.boss_group, False)
            if hit_boss:
                bullet.kill()
                for boss in hit_boss:
                    if boss.take_damage():
                        self._defeat_boss()
                    else:
                        ft = FloatText(boss.rect.centerx, boss.rect.top,
                                       "-1", RED)
                        self.float_texts.add(ft)
                        self.all_sprites.add(ft)
                continue

    # ============================================================
    # 绘制（每一帧）
    # ============================================================
    def draw(self):
        """绘制当前帧的画面"""
        # 背景
        self.screen.fill(SKY_BLUE)

        if self.state == self.STATE_MENU:
            # 菜单画面
            self.ui.draw_menu(self.screen)

        elif self.state in (self.STATE_PLAYING, self.STATE_PAUSED, self.STATE_GAMEOVER, self.STATE_WIN):
            # 根据摄像机偏移绘制所有精灵
            for sprite in self.all_sprites:
                # 计算屏幕上的位置（世界坐标 - 摄像机偏移）
                screen_rect = sprite.rect.copy()
                screen_rect.x -= self.camera_x

                # 只绘制屏幕内的（优化性能）
                if screen_rect.right < -50 or screen_rect.left > SCREEN_WIDTH + 50:
                    continue
                if screen_rect.bottom < -50 or screen_rect.top > SCREEN_HEIGHT + 50:
                    continue

                # 玩家无敌时闪烁效果
                if sprite == self.player and self.player.invincible > 0:
                    # 每 6 帧闪烁一次（60帧/6 = 每秒10次闪烁）
                    if (self.player.invincible // 6) % 2 == 0:
                        self.screen.blit(sprite.image, screen_rect)
                else:
                    self.screen.blit(sprite.image, screen_rect)

            # 绘制 HUD
            self.ui.draw_hud(self.screen, self.player, self.camera_x, self.level_name)

            # 绘制 Boss 生命条
            if self.boss_group:
                boss = list(self.boss_group)[0]
                if boss.health > 0:
                    self.ui.draw_boss_health(self.screen, boss, self.camera_x)

            # 暂停时叠加暂停菜单
            if self.state == self.STATE_PAUSED:
                self.ui.draw_pause_menu(self.screen)

            # 绘制死亡/通关覆盖层
            if self.state == self.STATE_GAMEOVER:
                self.ui.draw_gameover(self.screen, self.player)
            elif self.state == self.STATE_WIN:
                self.ui.draw_win(self.screen, self.player)

        # 刷新屏幕
        pygame.display.flip()

    # ============================================================
    # 主循环
    # ============================================================
    def run(self):
        """游戏主循环 —— 一直循环直到用户退出"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        # 退出游戏
        pygame.quit()
        sys.exit()


# ============================================================
# 程序入口
# ============================================================
if __name__ == "__main__":
    game = Game()
    game.run()
