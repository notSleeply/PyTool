import tkinter as tk
from tkinter import filedialog
import requests
import base64
from PIL import Image, ImageTk
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="673419c95524a124d1cfd60e8b19745c.KTLWvxYKpRa481Fz")  # 填写您自己的APIKey

# 上传图片的函数
def upload_image():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if image_path:
        with open(image_path, 'rb') as img_file:
            img_base = base64.b64encode(img_file.read()).decode('utf-8')
        response = client.chat.completions.create(
            model="glm-4v-flash",  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "从右边数第二个办公椅上有没有人？"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": img_base
                            }
                        }
                    ]
                }
            ]
        )
        global tk_image
        # 使用PIL库打开图片
        pil_image = Image.open(image_path)
        # 调整图片大小（可根据实际需求选择是否调整及调整的尺寸，这里示例调整为300x300）
        pil_image = pil_image.resize((300, 300), Image.Resampling.LANCZOS)
        # 将PIL图像转换为Tkinter可用的PhotoImage对象
        tk_image = ImageTk.PhotoImage(pil_image)
        # 更新Label组件显示新的图片
        image_label.configure(image=tk_image)

        print(response.chices[0].message)
        result_label.config(text=response.chices[0].message.content[0])
    else:
        result_label.config(text="未选择图片文件")


# 创建主窗口
root = tk.Tk()
root.title("AI分析图片")

# 创建按钮
upload_button = tk.Button(root, text="选择图片并上传", command=upload_image)
upload_button.pack(pady=20)

# 创建一个Label组件用于显示图片
tk_image = None
image_label = tk.Label(root)
image_label.pack()

# 创建用于显示结果的标签
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
