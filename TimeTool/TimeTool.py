import time
import tkinter as tk  # 用于创建图形用户界面（GUI）
from tkinter import messagebox # 用于在GUI中显示消息框。

reminder_message = "睡觉 (¦3[▓▓] 晚安!"  # 提醒内容
reminder_time_seconds = 3  # 提醒时间（秒）


# 设置提醒函数
def set_reminder(message, seconds):
    print(f"{seconds} 秒后将弹出提醒.")  # 打印提醒设置成功
    time.sleep(seconds)  # 等待指定时间
    show_popup(message)  # 弹出提醒窗口


# 弹窗提醒函数
def show_popup(message):
    root = tk.Tk()  # 创建一个Tkinter根窗口
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo("提醒", message)  # 弹出信息窗口
    root.destroy()  # 销毁主窗口


# 设定提醒
set_reminder(reminder_message, reminder_time_seconds)
