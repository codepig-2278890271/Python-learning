"""
============================================================
 🐍 Python 零基础入门 —— 11：异常处理
============================================================
 学习顺序：这是第 11 个文件（前提：已完成 10_面向对象编程入门.py）
 下一个文件：12_综合练习与小项目.py

 本节学习目标：
   ✅ 理解什么是异常
   ✅ 学会用 try/except 捕获和处理错误
   ✅ 掌握 else 和 finally 的用法
   ✅ 写出更健壮的程序
============================================================
"""

# ============================================================
# 第十六章：异常处理 —— 优雅地处理错误
# ============================================================
print("\n" + "=" * 60)
print("第十六章：异常处理")
print("=" * 60)

"""
程序运行时可能会出错（比如除以零、文件不存在、类型不对）。
如果不管这些错误，程序会直接崩溃。
try/except 可以"捕获"错误并妥善处理，让程序继续运行。
"""

# 不加处理的情况（注释掉以免中断整个程序）：
# result = 10 / 0   # 这行会报错：ZeroDivisionError

# ----- 用 try/except 捕获错误 -----
print("例子1：安全地做除法")
a, b = 10, 0

try:
    result = a / b
    print(f"{a} / {b} = {result}")
except ZeroDivisionError:
    print(f"  错误：不能除以零！{a} / {b} 没有意义。")

print("程序继续运行……")

# ----- 多个 except -----
def safe_divide(x, y):
    """安全除法——处理各种情况"""
    try:
        result = x / y
        print(f"  {x} / {y} = {result}")
        return result
    except ZeroDivisionError:
        print("  数学错误：除数不能是 0！")
    except TypeError:
        print("  类型错误：请传入数字！")
    except Exception as e:
        print(f"  未知错误：{e}")

print("\n例子2：多种错误处理")
safe_divide(10, 2)      # 正常
safe_divide(10, 0)      # 除以零
safe_divide("10", 2)    # 类型不对

# ----- try/except/else/finally -----
print("\n例子3：完整的异常处理结构")
try:
    num = int("123")         # 尝试转换
except ValueError:
    print("  转换失败，不是数字")
else:
    print(f"  转换成功！数字是 {num}")   # 没出错时执行
finally:
    print("  无论是否出错，我都会执行")    # 无论如何都执行

print("\n" + "=" * 60)
print("✅ 本文件学习完成！接下来请打开：12_综合练习与小项目.py")
print("=" * 60)
