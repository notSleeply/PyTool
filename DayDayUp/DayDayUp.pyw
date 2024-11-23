# 工具打包
# pip install pyinstaller
# pyinstaller --onefile --windowed DayDayUp.pyw  # 生成可执行文件

# ========== 导入必要模块 ========== #
import tkinter as tk  # 用于创建图形用户界面
import random  # 提供随机选择功能
import os  # 用于文件操作
import sys  # 系统操作
from pystray import Icon, MenuItem, Menu  # 创建系统托盘图标
from PIL import Image  # 图像处理
from tkinter import messagebox  # 创建消息弹窗
from win11toast import toast  # 实现桌面通知功能

# ========== 配置参数 ========== #
# 随机时间间隔 (单位: 毫秒)
TIME_RANDOM = 600000  # 每10分钟更新一次语录
WORD_LENGTH = 100  # 限制语录的最大字符长度
QUOTE_FILE = "Bible.txt"  # 默认语录存储文件
ICON_FILE = "icon.ico"  # 托盘图标文件路径
WINDOW_WIDTH = 1100  # 窗口宽度
WINDOW_HEIGHT = 500  # 窗口高度
MIN_WINDOW_WIDTH = 800  # 最小宽度
MIN_WINDOW_HEIGHT = 500  # 最小高度

# ========== 初始化语录 ========== #
# 检查语录文件是否存在，不存在则初始化默认语录
quotes = []
if os.path.exists(QUOTE_FILE):
    with open(QUOTE_FILE, "r", encoding="utf-8") as file:
        quotes = [line.strip() for line in file]  # 从文件读取语录
else:
    quotes = ["为了明天的你", "我爱你，孙浩男"]  # 默认语录

# 保存语录到文件
def save_quotes():
    with open(QUOTE_FILE, "w", encoding="utf-8") as file:
        file.writelines(f"{quote}\n" for quote in quotes)

# ========== 随机语录功能 ========== #
# 仅更新语录显示，不触发通知
def update_quote_only():
    quote = random.choice(quotes)  # 随机选取语录
    formatted_quote = quote.replace(".", "\n").replace("：", "\n")  # 格式化
    label.config(text=formatted_quote)

# 更新语录并显示通知
def show_quote():
    quote = random.choice(quotes)
    formatted_quote = quote.replace(".", "\n").replace("：", "\n")
    label.config(text=formatted_quote)
    toast("励志话语", formatted_quote, duration="short")  # 弹出桌面通知
    window.after(TIME_RANDOM, show_quote)  # 定时更新语录

# ========== 添加新语录 ========== #
def add_quote():
    # 内部函数：保存新语录
    def save_new_quote():
        new_quote = entry.get().strip()  # 获取用户输入
        if not new_quote:
            messagebox.showwarning("警告", "输入不能为空！")  # 输入校验
        elif len(new_quote) > WORD_LENGTH:
            messagebox.showwarning("警告", f"输入的语录不能超过{WORD_LENGTH}个字符！")
        else:
            quotes.append(new_quote)  # 添加到语录列表
            save_quotes()  # 保存到文件
            entry_window.destroy()  # 关闭输入窗口

    # 创建输入窗口
    entry_window = tk.Toplevel(window)
    entry_window.title("添加新话语")
    tk.Label(entry_window, text=f"请输入新的话语（不超过{WORD_LENGTH}个字符）：").pack(pady=5)
    entry = tk.Entry(entry_window, width=40)  # 输入框
    entry.pack(padx=10, pady=10)
    tk.Button(entry_window, text="保存", command=save_new_quote).pack(pady=5)

# ========== 退出功能 ========== #
def quit_app():
    global icon
    if icon:
        icon.stop()  # 停止托盘图标
    window.quit()  # 关闭窗口
    sys.exit()  # 退出程序

def on_window_close():
    quit_app()

def on_window_cover():
    window.withdraw()  # 隐藏窗口

def show_window(icon=None, item=None):
    window.deiconify()  # 显示窗口

# ========== 系统托盘功能 ========== #
def create_tray_icon():
    global icon
    try:
        icon_image = Image.open(ICON_FILE)  # 加载托盘图标
        icon = Icon(
            "励志话语", icon=icon_image,
            menu=Menu(
                MenuItem("显示", show_window),
                MenuItem("隐藏", on_window_cover),
                MenuItem("退出", quit_app)
            )
        )
        icon.run_detached()  # 运行托盘图标
        icon.visible = True
        icon.left_click = show_window  # 单击显示窗口
    except Exception as e:
        messagebox.showerror("错误", f"加载托盘图标失败: {e}")
        sys.exit()

# ========== 主窗口设置 ========== #
def update_wraplength(event):
    new_width = event.width - 5  # 自动调整文字换行
    if new_width > MIN_WINDOW_WIDTH:
        label.config(wraplength=new_width)

if __name__ == "__main__":
    # 创建主窗口
    window = tk.Tk()
    window.title("励志话语")
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")  # 设置窗口大小
    window.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)  # 设置最小尺寸
    window.resizable(True, True)  # 窗口大小可调整
    window.protocol("WM_DELETE_WINDOW", on_window_close)  # 自定义关闭事件

    # 显示语录的标签
    label = tk.Label(
        window, text=random.choice(quotes),
        font=("Microsoft YaHei", 24),
        padx=10, pady=20,
        wraplength=WINDOW_WIDTH, justify="center"
    )
    label.pack()

    # 绑定窗口尺寸调整事件
    window.bind("<Configure>", update_wraplength)

    # 底部按钮
    tk.Button(window, text="关闭", command=on_window_close, font=("Microsoft YaHei", 12)).pack(side=tk.BOTTOM, pady=10)
    tk.Button(window, text="隐藏", command=on_window_cover, font=("Microsoft YaHei", 12)).pack(side=tk.BOTTOM, pady=10)

    # 功能按钮框
    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM, pady=10)
    tk.Button(button_frame, text="随机话语", command=update_quote_only, font=("Microsoft YaHei", 12)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="添加话语", command=add_quote, font=("Microsoft YaHei", 12)).pack(side=tk.LEFT, padx=10)

    # 创建托盘图标并启动主循环
    create_tray_icon()
    show_quote()
    window.mainloop()
