"""
============================================================
 🎮 超级小猫 —— ui.py
 用户界面相关函数（菜单、HUD、结束画面等）
============================================================
 这里负责游戏逻辑之外的"界面层"：
   - 开始菜单（标题画面）
   - 游戏中 HUD（分数、生命、关卡名）
   - 死亡画面
   - 通关画面

 所有函数接收 screen 参数，直接在屏幕上绘制。

 改进思路：
   - 想换字体？把 font 改成从文件加载的字体
   - 想加按钮？在这里加 Button 类
   - 想加过场动画？在这里写过渡效果
============================================================
"""

import pygame
from settings import *


class UI:
    """UI 管理器 —— 统一管理字体和界面绘制"""

    def __init__(self):
        # 不同大小的字体
        _font = "Noto Sans CJK SC"
        self.font_small = pygame.font.SysFont(_font, 16)
        self.font_normal = pygame.font.SysFont(_font, 24)
        self.font_large = pygame.font.SysFont(_font, 48, bold=True)
        self.font_title = pygame.font.SysFont(_font, 64, bold=True)

        # 暂停菜单按钮（矩形区域，用于鼠标碰撞检测）
        self._pause_buttons = []

    def draw_text(self, screen, text, font, color, x, y, center=True):
        """
        在屏幕上绘制文字。

        参数:
            screen: pygame 窗口
            text: 要显示的文字
            font: pygame Font 对象
            color: 文字颜色（RGB 元组）
            x, y: 坐标
            center: True 表示 (x, y) 是文字中心；False 表示左上角
        """
        surface = font.render(text, True, color)
        if center:
            rect = surface.get_rect(center=(x, y))
        else:
            rect = surface.get_rect(topleft=(x, y))
        screen.blit(surface, rect)
        return rect

    # ============================================================
    # 开始菜单
    # ============================================================
    def draw_menu(self, screen):
        """绘制开始菜单画面"""
        # 蓝绿渐变背景
        screen.fill(SKY_BLUE)
        # 画一些装饰性"平台"
        for i in range(5):
            x = 100 + i * 150
            y = 300 + (i % 2) * 60
            pygame.draw.rect(screen, PLATFORM_BROWN, (x, y, 100, 20))
            pygame.draw.rect(screen, PLATFORM_TOP, (x, y, 100, 6))

        # 标题
        self.draw_text(screen, "🐱 超级小猫 🐱", self.font_title, WHITE,
                       SCREEN_WIDTH // 2, 150)
        # 标题阴影
        self.draw_text(screen, "🐱 超级小猫 🐱", self.font_title, BLACK,
                       SCREEN_WIDTH // 2 + 2, 152)

        # 小猫角色预览（放大版，与新外观一致）
        preview = pygame.Surface((PLAYER_WIDTH * 3, PLAYER_HEIGHT * 3), pygame.SRCALPHA)
        pw, ph = PLAYER_WIDTH * 3, PLAYER_HEIGHT * 3
        # 耳朵
        pygame.draw.polygon(preview, PLAYER_FUR, [(12, 24), (30, 0), (42, 24)])
        pygame.draw.polygon(preview, PLAYER_FUR, [(pw - 42, 24), (pw - 30, 0), (pw - 12, 24)])
        # 脸
        pygame.draw.ellipse(preview, PLAYER_FUR, (6, 12, pw - 12, 48))
        pygame.draw.ellipse(preview, PLAYER_BELLY, (18, 28, pw - 36, 30))
        # 眼睛
        pygame.draw.ellipse(preview, WHITE, (22, 26, 20, 20))
        pygame.draw.ellipse(preview, PLAYER_EYE, (28, 28, 12, 14))
        pygame.draw.ellipse(preview, WHITE, (pw - 42, 26, 20, 20))
        pygame.draw.ellipse(preview, PLAYER_EYE, (pw - 40, 28, 12, 14))
        # 鼻子
        nose_x, nose_y = pw // 2 - 6, 46
        pygame.draw.ellipse(preview, (255, 150, 150), (nose_x, nose_y, 12, 8))
        # 帽子
        pygame.draw.rect(preview, PLAYER_HAT, (6, 0, pw - 12, 22))
        # 身体
        pygame.draw.ellipse(preview, PLAYER_FUR, (12, 60, pw - 24, ph - 80))
        pygame.draw.ellipse(preview, PLAYER_BELLY, (24, 70, pw - 48, ph - 100))
        screen.blit(preview, (SCREEN_WIDTH // 2 - pw // 2, 180))

        # 操作说明
        instructions = [
            "🎮 操作说明 🎮",
            "",
            "A / D    —  左右移动",
            "K        —  跳跃",
            "J        —  发射子弹",
            "ESC      —  暂停游戏",
            "",
            "💡 踩敌人头顶或用子弹消灭敌人",
            "🪙 收集金币获得分数",
            "🏁 到达右侧旗帜即可通关！",
            "",
            "⚠️ 小心别掉进坑里哦！",
        ]
        for i, line in enumerate(instructions):
            self.draw_text(screen, line, self.font_small, WHITE,
                           SCREEN_WIDTH // 2, 340 + i * 22)

        # 闪烁的"按任意键开始"
        if pygame.time.get_ticks() % 1000 < 700:  # 0.7秒亮，0.3秒灭
            self.draw_text(screen, "按任意键开始游戏！", self.font_large, YELLOW,
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)

    # ============================================================
    # 游戏中 HUD（抬头显示）
    # ============================================================
    def draw_hud(self, screen, player, camera_x, level_name):
        """
        绘制游戏中 HUD：分数、生命、关卡名。

        参数:
            player: 玩家对象（读取 score 和 lives）
            camera_x: 摄像机水平偏移（HUD 不受卷轴影响）
            level_name: 当前关卡名称
        """
        # 半透明背景条
        hud_bg = pygame.Surface((SCREEN_WIDTH, 35), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 100))
        screen.blit(hud_bg, (0, 0))

        # 分数
        self.draw_text(screen, f"🪙 {player.score}",
                       self.font_normal, YELLOW, 120, 18)
        # 生命
        self.draw_text(screen, f"❤️ x {player.lives}",
                       self.font_normal, RED, 280, 18)
        # 关卡名
        self.draw_text(screen, level_name,
                       self.font_small, WHITE, SCREEN_WIDTH // 2, 18)

    # ============================================================
    # 死亡画面
    # ============================================================
    def draw_gameover(self, screen, player):
        """绘制游戏结束画面"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        self.draw_text(screen, "💀 游戏结束 💀", self.font_title, RED,
                       SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        self.draw_text(screen, f"最终得分: {player.score}", self.font_large, WHITE,
                       SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        self.draw_text(screen, "按 R 重新开始   按 Q 退出", self.font_normal, GRAY,
                       SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)

    # ============================================================
    # 通关画面
    # ============================================================
    def draw_win(self, screen, player):
        """绘制通关画面"""
        # 金色遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 215, 0, 160))
        screen.blit(overlay, (0, 0))

        self.draw_text(screen, "🎉 恭喜通关！🎉", self.font_title, RED,
                       SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        self.draw_text(screen, f"最终得分: {player.score}", self.font_large, WHITE,
                       SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.draw_text(screen, f"剩余生命: {player.lives}", self.font_normal, WHITE,
                       SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 35)
        self.draw_text(screen, "按 R 重新挑战   按 Q 退出", self.font_normal, GRAY,
                       SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)

    # ============================================================
    # Boss 生命条
    # ============================================================
    def draw_boss_health(self, screen, boss, camera_x):
        """
        在屏幕顶部绘制 Boss 生命条。

        参数:
            boss: Boss 对象（读取 health 和 max_health）
            camera_x: 摄像机偏移（条固定在屏幕顶部，不受卷轴影响）
        """
        if boss is None or boss.health <= 0:
            return

        bar_width = 400
        bar_height = 18
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 40

        # 背景条（深色）
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (40, 40, 40), bg_rect, border_radius=6)
        pygame.draw.rect(screen, (80, 80, 80), bg_rect, width=2, border_radius=6)

        # 血量条
        health_ratio = boss.health / boss.max_health
        fill_width = int(bar_width * health_ratio)

        # 颜色根据血量变化：绿 → 黄 → 红
        if health_ratio > 0.5:
            bar_color = (50, 200, 50)
        elif health_ratio > 0.25:
            bar_color = (220, 180, 30)
        else:
            bar_color = (220, 40, 40)

        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            pygame.draw.rect(screen, bar_color, fill_rect, border_radius=6)

        # Boss 名字
        self.draw_text(screen, "👑 暗黑魔王 👑", self.font_small, WHITE,
                       SCREEN_WIDTH // 2, bar_y - 12)

        # 血量文字
        hp_text = f"{boss.health}/{boss.max_health}"
        self.draw_text(screen, hp_text, self.font_small, WHITE,
                       SCREEN_WIDTH // 2, bar_y + bar_height + 10)

        # 阶段指示
        if boss.phase == 2:
            phase_text = "⚠️ 愤怒模式！⚠️"
            color = (255, 100, 50)
        else:
            phase_text = "阶段 1"
            color = (180, 180, 180)
        self.draw_text(screen, phase_text, self.font_small, color,
                       SCREEN_WIDTH // 2, bar_y + bar_height + 26)

    # ============================================================
    # 暂停菜单
    # ============================================================
    def get_pause_buttons(self):
        """
        返回暂停菜单中两个按钮的 Rect 列表，供 main.py 做鼠标点击检测。
        返回: [(button_name, pygame.Rect), ...]
        """
        btn_w, btn_h = 220, 50
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        resume_rect = pygame.Rect(center_x - btn_w // 2, center_y - 10, btn_w, btn_h)
        quit_rect = pygame.Rect(center_x - btn_w // 2, center_y + 60, btn_w, btn_h)

        self._pause_buttons = [
            ("resume", resume_rect),
            ("quit", quit_rect),
        ]
        return self._pause_buttons

    def draw_pause_menu(self, screen):
        """绘制暂停菜单（半透明遮罩 + 两个按钮）"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # 标题
        self.draw_text(screen, "⏸️ 游戏暂停", self.font_title, WHITE,
                       SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        # 获取按钮区域
        buttons = self.get_pause_buttons()

        # 检测鼠标悬停
        mouse_pos = pygame.mouse.get_pos()

        for name, rect in buttons:
            # 鼠标悬停时高亮
            color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            # 绘制按钮
            pygame.draw.rect(screen, color, rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, rect, width=2, border_radius=12)

            # 按钮文字
            if name == "resume":
                text = "▶  继续游戏"
            else:
                text = "✕  退出游戏"
            self.draw_text(screen, text, self.font_normal, BUTTON_TEXT,
                           rect.centerx, rect.centery)
