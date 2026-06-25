"""
============================================================
 🐍 Python 零基础入门 —— 10：面向对象编程入门
============================================================
 学习顺序：这是第 10 个文件（前提：已完成 09_文件操作.py）
 下一个文件：11_异常处理.py

 本节学习目标：
   ✅ 理解类和对象的概念
   ✅ 学会定义类、创建对象
   ✅ 掌握 __init__ 和 self 的含义
   ✅ 理解继承与重写
============================================================
"""

# ============================================================
# 面向对象编程（OOP）入门
# ============================================================
print("\n" + "=" * 60)
print("面向对象编程入门")
print("=" * 60)

"""
面向对象编程（OOP）是 Python 中非常重要的一种编程思想。

核心概念：
  - 类（Class）：就像一个"蓝图"或"模板"，定义了某类事物有什么属性、能做什么
  - 对象（Object）：根据蓝图造出来的具体实例
  - 属性：对象拥有的数据（比如狗的品种、年龄）
  - 方法：对象能做的事情（比如狗能叫、能跑）

类比：
  类 = 汽车的设计图纸
  对象 = 根据图纸造出来的那辆真车
"""

# ----- 定义一个简单的类 -----
class Dog:
    """一个简单的狗类"""

    # __init__ 是特殊方法：创建对象时自动调用
    # self 代表对象自己（必须写在第一个参数位置）
    def __init__(self, name, breed, age):
        self.name = name         # 属性：名字
        self.breed = breed       # 属性：品种
        self.age = age           # 属性：年龄

    # 方法：狗能做什么
    def bark(self):
        """狗叫"""
        print(f"{self.name}：汪汪！")

    def sit(self):
        """坐下"""
        print(f"{self.name} 坐下了。")

    def get_info(self):
        """获取狗的信息"""
        return f"{self.name}，{self.breed}，{self.age} 岁"

# ----- 创建对象并使用 -----
# 根据 Dog 类创建具体的狗
dog1 = Dog("旺财", "金毛", 3)
dog2 = Dog("小白", "柯基", 1)

print("狗的信息：")
print("  狗1：", dog1.get_info())
print("  狗2：", dog2.get_info())

print("\n狗的动作：")
dog1.bark()
dog1.sit()
dog2.bark()

# ----- 继承：子承父业 -----
class GuideDog(Dog):
    """导盲犬——继承自 Dog"""

    def __init__(self, name, breed, age, owner):
        super().__init__(name, breed, age)   # 调用父类的 __init__
        self.owner = owner                    # 新增属性：主人

    def work(self):
        """导盲犬的专属技能"""
        print(f"{self.name} 正在为 {self.owner} 引路……")

    # 重写（override）get_info 方法
    def get_info(self):
        base_info = super().get_info()
        return f"{base_info}，服务对象：{self.owner}"

guide_dog = GuideDog("忠诚", "拉布拉多", 2, "张大爷")
print("\n导盲犬信息：", guide_dog.get_info())
guide_dog.bark()         # 继承来的方法
guide_dog.work()         # 自己独有的方法

print("\n" + "=" * 60)
print("✅ 本文件学习完成！接下来请打开：11_异常处理.py")
print("=" * 60)
