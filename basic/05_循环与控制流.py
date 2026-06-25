"""
============================================================
 🐍 Python 零基础入门 —— 05：循环与控制流
============================================================
 学习顺序：这是第 5 个文件（前提：已完成 04_用户输入与条件判断.py）
 下一个文件：06_字符串操作.py

 本节学习目标：
   ✅ 掌握 for 循环和 range() 的用法
   ✅ 掌握 while 循环
   ✅ 理解 break 和 continue 的区别
   ✅ 小心死循环！
============================================================
"""

# ============================================================
# 循环 —— 让程序"重复做一件事"
# ============================================================
print("\n" + "=" * 60)
print("循环")
print("=" * 60)

"""
循环可以让一段代码重复执行多次。
Python 有两种主要的循环：
  1. for 循环 —— 遍历一个序列（比如遍历列表、字符串）
  2. while 循环 —— 只要条件成立就一直循环
"""

# ----- for 循环 -----
print("\n--- for 循环 ---")

# 遍历字符串（一个一个字符来）
print("逐个打印 'Python' 的每个字符：")
for letter in "Python":
    print("  ", letter)

# 用 range() 生成数字序列
# range(5) → 生成 0, 1, 2, 3, 4（从0开始，不包括5）
print("\n打印 0 到 4：")
for i in range(5):
    print("  第", i, "次")

# range(2, 7) → 生成 2, 3, 4, 5, 6（从2开始，到7之前结束）
print("\n打印 2 到 6：")
for i in range(2, 7):
    print("  数字:", i)

# range(1, 10, 2) → 生成 1, 3, 5, 7, 9（步长为2）
print("\n打印 1 到 9 的奇数：")
for i in range(1, 10, 2):
    print("  奇数:", i)

# 实际例子：打印乘法口诀表的一行
print("\n5 的乘法口诀：")
for i in range(1, 10):
    print("  5 ×", i, "=", 5 * i)

# ----- while 循环 -----
print("\n--- while 循环 ---")

# while 循环：只要条件成立就一直执行
print("倒数计时：")
countdown = 5
while countdown > 0:
    print("  ", countdown, "...")
    countdown = countdown - 1   # 每次减1（也可以写成 countdown -= 1）
print("  🚀 发射！")

# ⚠️ 小心死循环！下面这个永远停不下来（注释掉了）：
# while True:
#     print("我不会停！按 Ctrl+C 强制结束！")

# ----- break 和 continue -----
print("\n--- break 和 continue ---")

# break：立即退出循环
print("用 break 提前结束循环：")
for i in range(1, 11):
    if i == 6:
        print("  到 6 了，不玩了！")
        break               # 跳出循环
    print("  ", i)

# continue：跳过本次，继续下一次
print("\n用 continue 跳过偶数：")
for i in range(1, 11):
    if i % 2 == 0:          # 如果是偶数
        continue             # 跳过，不打印
    print("  奇数:", i)

print("\n" + "=" * 60)
print("✅ 本文件学习完成！接下来请打开：06_字符串操作.py")
print("=" * 60)
