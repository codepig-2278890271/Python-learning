"""
============================================================
 🐍 Python 零基础入门 —— 09：文件操作
============================================================
 学习顺序：这是第 9 个文件（前提：已完成 08_函数.py）
 下一个文件：10_面向对象编程入门.py

 本节学习目标：
   ✅ 学会用 open() 打开文件
   ✅ 掌握文件的读、写、追加操作
   ✅ 理解 with 语句（自动关闭文件）
   ✅ 了解不同的文件打开模式
============================================================
"""

# ============================================================
# 文件操作 —— 读写文件
# ============================================================
print("\n" + "=" * 60)
print("文件操作")
print("=" * 60)

"""
Python 可以轻松读写电脑上的文件。
最常见的就是读写 .txt 文件。

用 with 语句打开文件是最佳实践——它会自动关闭文件，不会忘记。
"""

# ----- 写文件 -----
print("正在写入文件...")
with open("test_hello.txt", "w", encoding="utf-8") as f:
    f.write("Hello, 这是用 Python 写的第一行文字！\n")
    f.write("这是第二行。\n")
    f.write("Python 文件操作很简单吧？\n")
    for i in range(1, 6):
        f.write(f"第 {i} 行自动生成的内容\n")

print("文件写入完成！生成了 test_hello.txt")

"""
open() 的模式：
  "r"  — 只读（read），文件不存在会报错
  "w"  — 只写（write），如果文件存在会覆盖！
  "a"  — 追加（append），在文件末尾添加
  "r+" — 读写
  encoding="utf-8" — 指定 UTF-8 编码以支持中文
"""

# ----- 读文件 -----
print("\n正在读取文件...")
with open("test_hello.txt", "r", encoding="utf-8") as f:
    content = f.read()          # read() 读取全部内容
    print("文件内容：")
    print(content)

# 逐行读取
print("逐行读取：")
with open("test_hello.txt", "r", encoding="utf-8") as f:
    for line_number, line in enumerate(f, 1):
        print(f"  第{line_number}行: {line.strip()}")  # strip() 去掉换行符

# 读取所有行到一个列表
print("\n用 readlines() 读取：")
with open("test_hello.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(f"  共 {len(lines)} 行")
    print(f"  第一行: {lines[0].strip()}")

print("\n" + "=" * 60)
print("✅ 本文件学习完成！接下来请打开：10_面向对象编程入门.py")
print("=" * 60)
