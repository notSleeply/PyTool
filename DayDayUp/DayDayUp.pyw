# 工具打包
# pip install pyinstaller
# pyinstaller --onefile --windowed DayDayUp.pyw  # 这将在dist文件夹中生成一个DayDayUp.exe文件。

import tkinter as tk  # 导入 tkinter，用于创建 GUI 界面
import random  # 导入 random 库，用于随机选择语录
import os  # 导入 os 库，用于文件操作
import sys  # 导入 sys 库，用于退出程序
from pystray import Icon, MenuItem, Menu  # 导入 pystray 库，用于创建系统托盘图标
from PIL import Image  # 导入 PIL 库，用于加载图标图片
from tkinter import messagebox  # 导入 tkinter 消息框，用于提示信息
from win11toast import toast # 桌面通知库

# 随机时间 单位ms
TimeRandom = 900000;

# 初始化语录列表。如果 quotes.txt 文件存在，则加载文件内容；否则，设置默认语录。
quotes = []
if os.path.exists("quotes.txt"):
    with open("quotes.txt", "r", encoding="utf-8") as file:
        quotes = [line.strip() for line in file]  # 去除每行的空格，并存入 quotes 列表
else:
    quotes = ["为了明天的你", "我爱你，孙浩男"]  # 默认语录内容


# 将当前 quotes 列表保存到 "quotes.txt" 文件中。
def save_quotes():
    with open("quotes.txt", "w", encoding="utf-8") as file:
        file.writelines(f"{quote}\n" for quote in quotes)  # 将 quotes 中的每条语录逐行写入文件


# 定义显示随机语录的函数，从 quotes 列表中选择并更新主窗口标签的文本内容。
def show_quote():
    # 显示随机语录在主窗口标签上
    quote = random.choice(quotes)
    label.config(text=quote)

    # 发送桌面通知
    toast("励志话语", quote, duration="short")

    # 定时调用 show_quote
    window.after(TimeRandom, show_quote)


# 定义添加新语录的函数，弹出窗口让用户输入并保存到 quotes 列表和文件中。
def add_quote():
    # 内部函数：获取用户输入并保存新语录
    def save_new_quote():
        new_quote = entry.get().strip()  # 获取并去除输入中的空格
        if not new_quote:
            messagebox.showwarning("警告", "输入不能为空！")  # 如果输入为空，弹出警告
        elif len(new_quote) > 25:
            messagebox.showwarning("警告", "输入的语录不能超过25个字符！")  # 如果输入超过25个字符，弹出警告
        else:
            quotes.append(new_quote)  # 添加新语录到 quotes 列表
            save_quotes()  # 保存更新后的语录列表到文件
            entry_window.destroy()  # 关闭输入窗口

    # 创建一个输入新语录的子窗口
    entry_window = tk.Toplevel(window)
    entry_window.title("添加新话语")
    tk.Label(entry_window, text="请输入新的话语（不超过25个字符）：").pack(pady=5)  # 输入提示标签
    entry = tk.Entry(entry_window, width=40)  # 创建输入框
    entry.pack(padx=10, pady=10)
    tk.Button(entry_window, text="保存", command=save_new_quote).pack(pady=5)  # 创建保存按钮，绑定保存函数


# 定义退出应用程序的函数，包含停止托盘图标、关闭主窗口、完全退出程序
def quit_app():
    global icon  # 声明 icon 为全局变量，以便在函数中操作托盘图标
    if icon:
        icon.stop()  # 停止托盘图标
    window.quit()  # 关闭 Tkinter 主窗口
    sys.exit()  # 彻底退出程序


# 定义窗口关闭事件，将关闭按钮绑定到 quit_app 函数，确保程序完全退出
def on_window_close():
    quit_app()  # 调用 quit_app 以关闭程序和托盘图标


# 隐藏窗口的函数
def on_window_cover():
    window.withdraw()  # 隐藏主窗口，不影响 Tkinter 主循环


# 显示主窗口的函数，用于托盘图标菜单点击后显示主窗口
def show_window(icon=None, item=None):
    window.deiconify()  # 取消窗口的隐藏状态，显示主窗口


# 创建托盘图标及其菜单，定义显示和退出菜单项
def create_tray_icon():
    global icon  # 声明全局变量 icon，以便其他函数访问
    try:
        icon_image = Image.open("icon.ico")  # 加载图标文件

        # 创建托盘图标并设置菜单项
        icon = Icon("励志话语", icon=icon_image,
                    menu=Menu(MenuItem("显示", show_window), MenuItem("隐藏", on_window_cover),
                              MenuItem("退出", quit_app)))

        # 绑定左键点击事件，用于显示窗口
        icon.run_detached()
        icon.visible = True  # 显示图标
        icon.left_click = show_window  # 设置左键点击事件为显示窗口
    except Exception as e:
        messagebox.showerror("错误", f"加载托盘图标失败: {e}")  # 若图标加载失败，弹出错误消息
        sys.exit()  # 退出程序

if __name__ == "__main__":
    # 创建 Tkinter 主窗口，并设置标题、尺寸和窗口关闭事件
    window = tk.Tk()
    window.title("励志话语")
    window.geometry("650x350")  # 设置窗口大小
    window.resizable(False, False)  # 禁止调整窗口大小
    window.protocol("WM_DELETE_WINDOW", on_window_close)  # 捕捉关闭事件

    # 创建显示语录的标签，初始化为随机语录，设置字体、边距和对齐方式
    label = tk.Label(window, text=random.choice(quotes), font=("Arial", 24), padx=10, pady=20, wraplength=500,
                     justify="center")
    label.pack()

    # 创建“关闭”和“隐藏”按钮，分别绑定 on_window_close 和 on_window_cover 函数
    tk.Button(window, text="关闭", command=on_window_close).pack(side=tk.BOTTOM, pady=10)
    tk.Button(window, text="隐藏", command=on_window_cover).pack(side=tk.BOTTOM, pady=10)

    # 创建底部按钮框架，包含“随机话语”和“添加话语”按钮
    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM, pady=10)
    tk.Button(button_frame, text="随机话语", command=show_quote).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="添加话语", command=add_quote).pack(side=tk.LEFT, padx=10)

    # 启动托盘图标
    create_tray_icon()

    # 初次调用 show_quote，以便定时器生效
    show_quote()

    # 运行 Tkinter 主循环，保持界面响应
    window.mainloop()