"""
============================================================
 🐍 Python 零基础入门 —— 07：列表、元组、字典、集合
============================================================
 学习顺序：这是第 7 个文件（前提：已完成 06_字符串操作.py）
 下一个文件：08_函数.py

 本节学习目标：
   ✅ 掌握列表的创建、访问、修改和遍历
   ✅ 理解元组和列表的区别（可变 vs 不可变）
   ✅ 学会用字典存储键值对
   ✅ 了解集合的用途（去重、集合运算）
============================================================
"""

# ============================================================
# 第十章：列表 —— 装东西的"篮子"
# ============================================================
print("\n" + "=" * 60)
print("第十章：列表 (list)")
print("=" * 60)

"""
列表是 Python 中最常用的数据结构。
想象一个购物清单，上面按顺序列着你要买的东西——这就是列表。

特点：
  - 用方括号 [] 表示
  - 元素之间有顺序
  - 可以放任何类型（数字、字符串、甚至另一个列表）
  - 可以随时增删改
"""

# 创建列表
shopping_list = ["牛奶", "鸡蛋", "面包", "苹果"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, 3.14, True]   # 混合类型
empty = []                            # 空列表

print("购物清单:", shopping_list)
print("混合列表:", mixed)

# ----- 访问元素（索引从 0 开始！）-----
print("\n--- 索引（下标）---")
fruits = ["苹果", "香蕉", "橘子", "葡萄", "西瓜"]
print("完整列表:", fruits)
print("第 1 个 fruits[0]:", fruits[0])    # 索引从 0 开始！
print("第 3 个 fruits[2]:", fruits[2])
print("最后1个 fruits[-1]:", fruits[-1])   # 负数索引：从末尾倒数
print("倒数第2 fruits[-2]:", fruits[-2])

# ----- 切片（取一段）-----
print("\n--- 切片 ---")
# 语法：列表[开始:结束:步长]  注意：结束位置不包含！
print("fruits[1:3]（第2到第3个）:", fruits[1:3])     # 索引1到3（不含3）
print("fruits[:3]（前3个）:", fruits[:3])             # 从头到索引3
print("fruits[2:]（从第3个到末尾）:", fruits[2:])     # 索引2到末尾
print("fruits[::2]（每隔一个取）:", fruits[::2])      # 每隔两个取一个

# ----- 修改列表 -----
print("\n--- 修改列表 ---")
colors = ["红", "绿", "蓝"]
print("原始:", colors)

# 添加元素
colors.append("黄")             # 在末尾添加
print("append 后:", colors)

colors.insert(1, "橙")          # 在索引1的位置插入
print("insert 后:", colors)

# 删除元素
colors.remove("绿")             # 删除指定值（注意：只删第一个匹配的）
print("remove 后:", colors)

removed = colors.pop()          # 弹出（删除并返回）最后一个
print("pop 后:", colors, "弹出的:", removed)

del colors[0]                   # 用 del 删除指定索引
print("del 后:", colors)

# ----- 列表常用操作 -----
print("\n--- 常用操作 ---")
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print("原始:", nums)
print("长度:", len(nums))
print("最大值:", max(nums))
print("最小值:", min(nums))
print("总和:", sum(nums))

nums.sort()                     # 排序（直接修改原列表）
print("排序后:", nums)

nums.reverse()                  # 反转
print("反转后:", nums)

print("5 出现了几次:", nums.count(5))   # 计数
print("5 在哪个位置:", nums.index(5))   # 查找索引（没找到会报错）

# ----- 遍历列表 -----
print("\n--- 遍历列表 ---")
for fruit in fruits:
    print(f"  我喜欢吃{fruit}")

# enumerate 同时获取索引和元素
for index, fruit in enumerate(fruits):
    print(f"  第 {index + 1} 个是 {fruit}")

# ----- 列表推导式（高级技巧，但很实用）-----
print("\n--- 列表推导式 ---")
# 一行代码生成一个列表
squares = [x**2 for x in range(1, 11)]   # 1到10的平方
print("1到10的平方:", squares)

even = [x for x in range(1, 21) if x % 2 == 0]  # 1到20中的偶数
print("1到20的偶数:", even)

# ============================================================
# 第十一章：元组和字典 —— 更多装东西的容器
# ============================================================
print("\n" + "=" * 60)
print("第十一章：元组 (tuple) 和字典 (dict)")
print("=" * 60)

# ----- 元组：不可修改的列表 -----
print("\n--- 元组 (tuple) ---")
"""
元组和列表很像，但有一个关键区别：
  元组创建后就不能再修改（增删改都不行）！
  用圆括号 () 表示。

什么时候用元组？
  - 数据不应该被修改的时候（比如坐标、RGB颜色值）
  - 作为字典的键（字典键必须是不可变类型）
"""

point = (3, 5)                    # 一个坐标
rgb = (255, 128, 0)               # 橙色
person = ("小明", 25, "北京")      # 姓名、年龄、城市

print("坐标:", point)
print("颜色:", rgb)
print("x坐标:", point[0])         # 访问和列表一样
print("y坐标:", point[1])

# 元组解包（一次性取出多个值）
name_tuple, age_tuple, city = person
print(f"{name_tuple} 今年 {age_tuple} 岁，住在 {city}")

# 下面这行会报错，因为元组不能改：
# point[0] = 10  # ❌ TypeError: 'tuple' object does not support item assignment

# ----- 字典：键值对的容器 -----
print("\n--- 字典 (dict) ---")
"""
字典用来存储"键-值"对。
就像一个真正的字典：你查"苹果"这个词（键），找到它的定义（值）。

特点：
  - 用花括号 {} 表示
  - 每个元素是 键: 值 的形式
  - 通过键来访问值（不是通过索引！）
  - 查找速度非常快
"""

# 创建字典
person_dict = {
    "姓名": "小明",
    "年龄": 25,
    "城市": "北京",
    "爱好": ["编程", "篮球", "音乐"]
}
print("个人信息字典:", person_dict)

# 访问值
print("\n姓名:", person_dict["姓名"])
print("年龄:", person_dict["年龄"])
print("爱好:", person_dict["爱好"])

# 用 get 方法访问（更安全：键不存在时不会报错）
print("电话:", person_dict.get("电话", "未填写"))  # 没这个键，返回默认值

# 修改和添加
person_dict["年龄"] = 26            # 修改已有键的值
person_dict["电话"] = "13800138000" # 添加新键值对
print("\n修改后:", person_dict)

# 删除
del person_dict["电话"]
print("删除电话后:", person_dict)

# 遍历字典
print("\n遍历字典:")
for key, value in person_dict.items():
    print(f"  {key} → {value}")

# 只遍历键
print("所有的键:", list(person_dict.keys()))
# 只遍历值
print("所有的值:", list(person_dict.values()))

# ============================================================
# 第十二章：集合
# ============================================================
print("\n" + "=" * 60)
print("第十二章：集合 (set)")
print("=" * 60)

"""
集合的特点：
  - 元素不能重复（自动去重！）
  - 元素没有顺序
  - 用花括号 {} 或 set() 创建
  - 可以做数学里的集合运算（交集、并集等）
"""

# 创建集合
fruits_set = {"苹果", "香蕉", "橘子", "苹果"}  # 重复的"苹果"自动去掉
print("集合（自动去重）:", fruits_set)

# 从列表去重
numbers_with_dup = [1, 2, 2, 3, 3, 3, 4, 5, 5]
unique_numbers = list(set(numbers_with_dup))
print("去重前:", numbers_with_dup)
print("去重后:", unique_numbers)

# 集合运算
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
print(f"\n集合 A: {a}")
print(f"集合 B: {b}")
print("交集 A & B:", a & b)     # 两个集合都有的
print("并集 A | B:", a | b)     # 两个集合合并
print("差集 A - B:", a - b)     # A有但B没有的
print("差集 B - A:", b - a)     # B有但A没有的

print("\n" + "=" * 60)
print("✅ 本文件学习完成！接下来请打开：08_函数.py")
print("=" * 60)
