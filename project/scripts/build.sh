#!/bin/bash
# ============================================================
# 一键编译脚本：把源码打包成独立可执行文件
# 用法：bash scripts/build.sh（在 project/ 目录下执行）
# ============================================================
set -e

# 切换到项目根目录（脚本在 scripts/ 下）
cd "$(dirname "$0")/.."

echo "🔨 正在编译 超级小猫 ..."
pyinstaller --onefile \
    --name "超级小猫" \
    --distpath build/bin \
    --workpath build/tmp \
    --specpath build \
    --paths src \
    src/main.py

rm -rf build/tmp
echo "✅ 编译完成！可执行文件：build/bin/超级小猫"
ls -lh build/bin/超级小猫
