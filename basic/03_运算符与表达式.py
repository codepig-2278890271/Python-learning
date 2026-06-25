"""
============================================================
 🐍 Python 零基础入门 —— 03：运算符与表达式
============================================================
 学习顺序：这是第 3 个文件（前提：已完成 02_变量与数据类型.py）
 下一个文件：04_用户输入与条件判断.py

 本节学习目标：
   ✅ 掌握算术运算符（加减乘除等）
   ✅ 理解比较运算符（大于、小于、等于等）
   ✅ 学会使用逻辑运算符（and、or、not）
   ✅ 了解字符串的拼接和重复
============================================================
"""

# ============================================================
# 第五章：运算 —— 加减乘除和更多
# ============================================================
print("\n" + "=" * 60)
print("第五章：运算符")
print("=" * 60)

# ----- 算术运算 -----
print("\n--- 算术运算 ---")
a = 10
b = 3

print("a =", a, ", b =", b)
print("加法 a + b =", a + b)      # 13
print("减法 a - b =", a - b)      # 7
print("乘法 a * b =", a * b)      # 30
print("除法 a / b =", a / b)      # 3.333... （结果是小数！）
print("整除 a // b =", a // b)    # 3 （只要整数部分）
print("取余 a % b =", a % b)      # 1 （10 除以 3 的余数）
print("幂 a ** b =", a ** b)      # 1000 （10 的 3 次方）

# ----- 比较运算（结果是 True 或 False）-----
print("\n--- 比较运算 ---")
x = 5
y = 8
print("x =", x, ", y =", y)
print("x == y ?", x == y)    # 等于（注意是两个等号！）
print("x != y ?", x != y)    # 不等于
print("x > y  ?", x > y)     # 大于
print("x < y  ?", x < y)     # 小于
print("x >= y ?", x >= y)    # 大于等于
print("x <= y ?", x <= y)    # 小于等于

"""
⚠️ 重要区别：
  一个等号 =   是赋值（把值放进去）
  两个等号 ==  是比较（左右两边相等吗？）
  这是新手最容易搞混的地方！
"""

# ----- 逻辑运算 -----
print("\n--- 逻辑运算 ---")
# and（与）：两边都 True 才是 True
print("True and True  =", True and True)    # True
print("True and False =", True and False)   # False

# or（或）：只要有一边 True 就是 True
print("True or False  =", True or False)    # True
print("False or False =", False or False)   # False

# not（非）：取反
print("not True  =", not True)              # False
print("not False =", not False)             # True

# 实际应用举例：
age = 20
has_ticket = True
can_enter = (age >= 18) and has_ticket
print("\n年龄:", age, "有票:", has_ticket, "→ 能入场:", can_enter)

# ----- 字符串也能"加"和"乘"-----
print("\n--- 字符串运算 ---")
first_name = "张"
last_name = "三"
full_name = first_name + last_name    # + 把字符串拼接起来
print("姓名:", full_name)

laugh = "哈"
print("大笑:", laugh * 5)             # * 把字符串重复多次

print("\n" + "=" * 60)
print("✅ 本文件学习完成！接下来请打开：04_用户输入与条件判断.py")
print("=" * 60)
