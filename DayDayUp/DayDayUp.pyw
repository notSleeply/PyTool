# 工具打包
# pip install pyinstaller
# pyinstaller --onefile --noconsole DayDayUp.pyw  这将在dist文件夹中生成一个DayDayUp.exe文件。

import tkinter as tk
import random
import os

quotes = []  # quotes.txt 文件相当于数据库

# 如果文件存在，则从文件中加载话语
if os.path.exists("quotes.txt"):
    with open("quotes.txt", "r", encoding="utf-8") as file:
        quotes = [line.strip() for line in file]
else:
    # 初始随机话语
    quotes = [
        "为了明天的你",
        "我爱你，孙浩男",
    ]

# 保存话语到文件
def save_quotes():
    with open("quotes.txt", "w", encoding="utf-8") as file:
        for quote in quotes:
            file.write(quote + "\n")

# 显示随机话语
def show_quote():
    # 从quotes列表中随机选择一个话语并显示在标签上
    quote = random.choice(quotes)
    label.config(text=quote)

# 添加新话语
def add_quote():
    # 添加新话语的窗口
    def save_new_quote():
        # 获取用户输入的新话语并保存
        new_quote = entry.get().strip()
        if new_quote:
            quotes.append(new_quote)
            save_quotes()  # 将新的话语保存到文件
            entry_window.destroy()
        else:
            tk.messagebox.showwarning("警告", "输入不能为空！")

    entry_window = tk.Toplevel(window)
    entry_window.title("添加新话语")
    tk.Label(entry_window, text="请输入新的话语：").pack(pady=5)
    entry = tk.Entry(entry_window, width=40)
    entry.pack(padx=10, pady=10)
    tk.Button(entry_window, text="保存", command=save_new_quote).pack(pady=5)

# 创建主窗口
window = tk.Tk()
window.title("励志话语")

# 设置固定窗口大小
window.geometry("550x250")
window.resizable(False, False)

# 显示初始话语，添加wraplength参数以控制宽度超出时自动换行
label = tk.Label(
    window, 
    text=random.choice(quotes), 
    font=("Arial", 20), 
    padx=20, 
    pady=20, 
    wraplength=500,  # 设置最大宽度为500像素，超出时换行
    justify="center"  # 设置文本居中对齐
)
label.pack()

# 随机话语按钮
random_button = tk.Button(window, text="随机话语", command=show_quote)
random_button.pack()

# 添加新话语按钮
add_button = tk.Button(window, text="添加话语", command=add_quote)
add_button.pack()

# 关闭按钮
close_button = tk.Button(window, text="关闭", command=window.quit)
close_button.pack()

# 运行主循环
window.mainloop()
