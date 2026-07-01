"""
============================================================
 🐍 Python 零基础入门 —— 12：综合练习与小项目
============================================================
 学习顺序：这是第 12 个文件（也是最后一个！前提：已完成前面所有文件）

 本节学习目标：
   ✅ 综合运用前面所学的知识
   ✅ 亲手实现猜数字游戏
   ✅ 实现待办事项管理器（面向对象）
   ✅ 编写实用工具函数
============================================================
"""

# ============================================================
# 综合练习 —— 做个实用小项目
# ============================================================
print("\n" + "=" * 60)
print("综合小练习")
print("=" * 60)

# ----- 练习1：猜数字游戏 -----
print("\n🎮 练习1：猜数字游戏（自动演示版）")
import random

def guess_number_game():
    """猜数字游戏"""
    target = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    print(f"  我想了一个 1~100 之间的数字，你有 {max_attempts} 次机会猜中它。")

    # 模拟几次猜测（真实版用 input()）
    simulated_guesses = [50, 75, 62, 68, 73, 71, 72]
    for guess in simulated_guesses:
        attempts += 1
        print(f"  第 {attempts} 次猜测：{guess}", end=" → ")

        if guess == target:
            print(f"🎉 恭喜！你猜中了！答案就是 {target}！用了 {attempts} 次。")
            return
        elif guess < target:
            print("太小了！往大猜。")
        else:
            print("太大了！往小猜。")

        if attempts >= max_attempts:
            print(f"  😢 次数用完了！答案是 {target}。")
            return

guess_number_game()

# ----- 练习2：待办事项管理器 -----
print("\n📋 练习2：待办事项管理器")

class TodoList:
    """简单的待办事项管理器"""

    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        """添加任务"""
        self.tasks.append({"task": task, "done": False})
        print(f"  ✅ 已添加：{task}")

    def complete_task(self, index):
        """完成任务"""
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = True
            print(f"  ✅ 已完成：{self.tasks[index]['task']}")
        else:
            print(f"  ❌ 无效的任务编号")

    def remove_task(self, index):
        """删除任务"""
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            print(f"  🗑️ 已删除：{removed['task']}")
        else:
            print(f"  ❌ 无效的任务编号")

    def show(self):
        """显示所有任务"""
        if not self.tasks:
            print("  📭 待办列表是空的！")
            return

        print(f"  📋 待办事项（共 {len(self.tasks)} 项）：")
        for i, item in enumerate(self.tasks, 1):
            status = "✅" if item["done"] else "⏳"
            print(f"    {i}. [{status}] {item['task']}")

# 演示
todo = TodoList()
todo.show()

todo.add_task("买牛奶")
todo.add_task("学 Python")
todo.add_task("跑步 30 分钟")
todo.add_task("给妈妈打电话")
todo.show()

todo.complete_task(1)   # 完成"学 Python"
todo.complete_task(2)   # 完成"跑步 30 分钟"
todo.remove_task(0)     # 删掉"买牛奶"
todo.show()

# ----- 练习3：实用工具函数合集 -----
print("\n🔧 练习3：实用工具函数")

def fahrenheit_to_celsius(f):
    """华氏度转摄氏度"""
    return (f - 32) * 5 / 9

def is_palindrome(text):
    """判断是否是回文（正着读反着读都一样）"""
    # 1. text.lower() → 全部转小写（让大小写不影响判断，如 "Racecar" 也能识别）
    # 2. .replace(" ", "") → 去掉所有空格（让 "a b a" 也能被识别为回文）
    cleaned = text.lower().replace(" ", "")
    # 切片 [::-1] 表示从后往前取，即把字符串反转
    # 比较清理后的字符串和它的反转是否相等
    return cleaned == cleaned[::-1]

def fibonacci(n):
    """生成斐波那契数列的前 n 项"""
    # 斐波那契数列：从 0, 1 开始，后面每一项都是前两项之和
    # 即：0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    fib = [0, 1]                       # 初始化前两项
    # _ 和 i 的区别：
    #   - i 是正常变量名，表示循环中会用到的索引值
    #   - _ 是 Python 惯例：告诉读代码的人“这个变量我不关心，仅仅用来凑循环次数”
    #   功能完全一样，但用 _ 更省内存（不会创建变量），也让代码意图更清晰
    for _ in range(2, n):              # 从第 3 项（索引 2）开始，生成到第 n 项
        # fib[-1] 是列表最后一个元素，fib[-2] 是倒数第二个
        # 每次循环把最后两项相加，追加到列表末尾
        fib.append(fib[-1] + fib[-2])
    return fib[:n]                     # 返回前 n 项（切片 [:n] 保证 n < 2 时也正确）

# 测试
print(f"  100°F = {fahrenheit_to_celsius(100):.1f}°C")
print(f"  '上海自来水来自海上' 是回文吗？ {is_palindrome('上海自来水来自海上')}")
print(f"  'hello' 是回文吗？ {is_palindrome('hello')}")
print(f"  斐波那契数列前 10 项：{fibonacci(10)}")


# ============================================================
# 🎉 恭喜你！
# ============================================================
print("\n" + "=" * 60)
print("🎉🎉🎉 恭喜你完成了 Python 基础教程！🎉🎉🎉")
print("=" * 60)

"""
你已经学了：
  ✅ 变量和数据类型
  ✅ 运算符
  ✅ 条件判断 if/elif/else
  ✅ 循环 for/while
  ✅ 字符串操作
  ✅ 列表、元组、字典、集合
  ✅ 函数
  ✅ 文件读写
  ✅ 类和对象（OOP基础）
  ✅ 异常处理

接下来该做什么？
  1. 把你学到的知识写几个小项目练手
  2. 学习第三方库：requests（爬虫）、flask（网站）、pandas（数据分析）
  3. 去 LeetCode 或 牛客网 刷几道简单题
  4. 最重要的：多写代码！编程是一门手艺活，不练是学不会的！

记住：
  - 不会就问 AI（Claude、ChatGPT…），AI 是程序员最好的搭档
  - 报错不可怕，读报错信息是编程的日常
  - 复制粘贴别人的代码前，先搞懂每行在干嘛
  - 保持好奇心，享受创造的乐趣！

加油，未来的 Python 高手！🚀
"""
