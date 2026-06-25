# 🐱 超级小猫 —— Python 横版跳跃游戏

一个使用 **Pygame** 开发的类超级玛丽风格横版跳跃游戏，适合作为 Python 学习项目长期迭代改进。

---

## 🎮 快速开始

### 方式一：直接运行可执行文件（推荐）
```bash
./build/bin/超级小猫
```
无需安装 Python，双击即可运行（Linux x86-64）。

### 方式二：源码运行
```bash
# 安装依赖
pip3 install pygame

# 启动游戏
cd project
python3 -m src.main          # 用包方式运行（python3 src/main.py 也可以）
```

---

## 🕹️ 操作说明

| 按键 | 功能 |
|------|------|
| **A / D** | 左右移动 |
| **K** | 跳跃 |
| **J** | 发射子弹 |
| **ESC** | 暂停 / 继续 |
| 鼠标点击 | 暂停菜单操作（继续游戏 / 退出） |

---

## 🎯 游戏目标

- 👾 踩敌人头顶或用子弹消灭敌人
- 🪙 收集金币获得分数
- 🏁 到达关卡最右侧的旗帜即可通关
- ❤️ 初始 3 条命，碰到敌人侧面或掉入坑中会扣命

---

## 📁 项目结构

```
project/
├── src/                     # 源代码
│   ├── main.py              # 游戏引擎 & 主循环
│   ├── settings.py          # 配置常量（调数值来这里！）
│   ├── sprites.py           # 精灵类（玩家、敌人、金币等）
│   ├── level.py             # 关卡数据定义
│   └── ui.py                # 界面：菜单、HUD、暂停面板
├── ui/                      # 图片、音效等资源文件
├── docs/                    # 文档
│   ├── README.md            # 本文件
│   └── 代码分析指南.md
├── scripts/                 # 工具脚本
│   ├── build.sh             # 一键编译脚本
│   └── run_windows.bat
├── build/                    # 编译产物
│   └── bin/                  # 可执行文件
│       └── 超级小猫         # 独立可执行文件
└── log/                     # 运行日志
```

---

## 🛠️ 编译为可执行文件

改完源码后，一键编译：
```bash
bash scripts/build.sh
```

或手动执行：
```bash
pip3 install pyinstaller
pyinstaller --onefile --name "超级小猫" --distpath build/bin --workpath build/tmp --specpath build --paths src src/main.py
rm -rf build/tmp
```

---

## 🔧 如何自定义

### 调整难度 / 手感
编辑 `src/settings.py`：
- `GRAVITY` — 重力大小（默认 0.8）
- `JUMP_POWER` — 跳跃力度（默认 -14，越负跳越高）
- `PLAYER_SPEED` — 移动速度（默认 5）
- `BULLET_SPEED` — 子弹速度（默认 6）
- `STARTING_LIVES` — 初始生命数（默认 3）

### 修改关卡
编辑 `src/level.py`，修改 `build_level_1()` 中的平台、金币、敌人坐标。

### 添加新关卡
在 `src/level.py` 中新建 `build_level_2()` 函数，然后在 `get_level()` 中注册。

### 更换外观
在 `src/sprites.py` 中找到各个 `_draw_xxx()` 方法，修改绘制代码；或替换为 `pygame.image.load("图片.png")`。

### 添加音效
在 `src/sprites.py` 或 `src/main.py` 中使用：
```python
sound = pygame.mixer.Sound("ui/jump.wav")
sound.play()
```

---

## 📝 迭代方向（TODO）

- [ ] 精灵图替换纯色方块
- [ ] 关卡编辑器
- [ ] 更多敌人类型（飞行怪、Boss）
- [ ] 道具系统（加速鞋、无敌星、磁铁）
- [ ] 音效 & 背景音乐
- [ ] 关卡选择界面
- [ ] 存档 & 读档
- [ ] 排行榜

---

## 🐛 问题反馈

遇到 Bug 或有改进建议？欢迎提 Issue 或直接改代码！

---

**加油，未来的 Python 高手！🚀**
