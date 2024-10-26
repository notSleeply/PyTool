# 工具打包
# pip install pyinstaller
# pyinstaller --onefile --noconsole DayDayUp.pyw  这将在dist文件夹中生成一个DayDayUp.exe文件。

import tkinter as tk
import random

# 一些随机的励志话语
quotes = [
    "为了明天的你",
    "我爱你，孙浩男",
    "一天只做一个功能",
    "只要努力，就会有收获",
    "梦想不是空想，而是追求",
    "今天的努力，明天的成就",
    "坚持就是胜利",
    "生活就像一杯茶，不会苦一辈子",
    "勤能补拙",
]

def show_quote():
    # 创建一个窗口
    window = tk.Tk()
    window.title("励志话语")

    # 随机选择一条话语
    quote = random.choice(quotes)

    # 在窗口中显示话语
    label = tk.Label(window, text=quote, font=("Arial", 20), padx=20, pady=20)
    label.pack()

    # 关闭窗口按钮
    button = tk.Button(window, text="关闭", command=window.quit)
    button.pack()

    window.mainloop()

if __name__ == "__main__":
    show_quote()
