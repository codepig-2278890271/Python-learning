"""
============================================================
 src 包初始化
============================================================
确保 src/ 目录在 Python 搜索路径中，这样 src/ 内的
模块可以相互 import（如 from settings import *）。

无论从哪个入口启动 ——
  - python run_game.py（启动器）
  - python -m src.main（包方式运行）
  - python main.py（直接在 src/ 下跑）

—— 都能正确找到同目录下的模块。
============================================================
"""
import os
import sys

_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)
