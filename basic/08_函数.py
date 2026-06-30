"""
============================================================
 🐍 Python 零基础入门 —— 08：函数
============================================================
 学习顺序：这是第 8 个文件（前提：已完成 07_列表元组字典集合.py）
 下一个文件：09_文件操作.py

 本节学习目标：
   ✅ 理解函数的定义和调用
   ✅ 掌握参数传递（位置参数、关键字参数、默认值）
   ✅ 学会用 return 返回值
   ✅ 体会函数如何让代码更整洁
============================================================
"""

# ============================================================
# 函数 —— 把代码打包复用
# ============================================================
print("\n" + "=" * 60)
print("函数")
print("=" * 60)

"""
函数是把一段代码"打包"起来，给它起个名字。
以后想用这段代码的时候，喊它的名字就行了，不用重写一遍。

这就像：
  - "刷牙"是一个功能——每次刷牙不用重新学习，直接执行这个动作就行
  - "泡方便面"是一个流程——有了这个函数，饿了就"调用"它

为什么用函数？
  1. 避免重复写同样的代码（DRY 原则：Don't Repeat Yourself）
  2. 让代码更有条理、更容易理解
  3. 修改时只需改一处
"""

# ----- 定义和调用函数 -----
def say_hello():
    """这是一个最简单的函数——打招呼"""
    print("你好！")
    print("欢迎学习 Python！")
    print("今天是美好的一天！")

# 调用函数（喊它的名字）
print("第一次调用：")
say_hello()

print("\n第二次调用：")
say_hello()

print()
# ----- 带参数的函数 -----
def greet(name):
    """向指定的人打招呼"""
    print(f"你好，{name}！")

greet("小明")
greet("小红")
greet("老师")
print()

# 多个参数
def introduce(name, age, hobby):
    """介绍一个人"""
    print(f"我叫{name}，今年{age}岁，喜欢{hobby}。")

introduce("小明", 25, "打篮球")
introduce("小红", 23, "画画")
# 也可以用"关键字参数"来调用（顺序可以不一样）
introduce(age=30, hobby="读书", name="老王")

# ----- 带默认值的参数 -----
def order_coffee(size="中杯", coffee_type="美式"):
    """点咖啡，默认中杯美式"""
    print(f"一杯{size}{coffee_type}，请慢用！")

order_coffee()                          # 全部用默认值
order_coffee("大杯")                    # 只改 size
order_coffee("小杯", "拿铁")            # 两个都改
order_coffee(coffee_type="卡布奇诺")    # 只改 coffee_type

# ----- 有返回值的函数 -----
def add(a, b):
    """计算两数之和并返回结果"""
    result = a + b
    return result   # return 把结果"丢回去"给调用者

sum_result = add(3, 5)
print(f"3 + 5 = {sum_result}")

# 更实用的例子
def calculate_bmi(weight_kg, height_m):
    """计算 BMI 指数"""
    bmi = weight_kg / (height_m ** 2)
    return bmi

def bmi_category(bmi):
    """根据 BMI 值判断类别"""
    if bmi < 18.5:
        return "偏瘦"
    elif bmi < 24:
        return "正常"
    elif bmi < 28:
        return "偏胖"
    else:
        return "肥胖"

# 使用这两个函数
my_bmi = calculate_bmi(70, 1.75)
my_category = bmi_category(my_bmi)
print(f"体重 70kg，身高 1.75m → BMI: {my_bmi:.1f}，类别: {my_category}")

print("\n" + "=" * 60)
print("✅ 本文件学习完成！接下来请打开：09_文件操作.py")
print("=" * 60)
