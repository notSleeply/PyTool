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
    "天道酬勤",
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
