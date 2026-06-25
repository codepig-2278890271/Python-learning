@echo off
chcp 65001 >nul
echo ================================
echo   🐱 超级小猫 - Windows 启动
echo ================================
echo.
echo 正在检查依赖...
pip install pygame 2>nul
echo.
echo 启动游戏中...
python -m src.main
pause
