import qrcode

# 参数设置
QR_VERSION = 1  # 版本号，二维码的尺寸大小
ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_L  # 纠错等级，L级别是7%纠错能力
BOX_SIZE = 10  # 每个格子的像素大小
BORDER_SIZE = 4  # 边框宽度
FILL_COLOR = 'black'  # 二维码前景色
BACK_COLOR = 'white'  # 二维码背景色
url = 'https://www.baidu.com' # 生成二维码的网址
PNG = 'qr.png' # 二维码图片名称

# 生成二维码的函数
def generate_qr(data, file_name):
    qr = qrcode.QRCode(
        version=QR_VERSION,  # 使用参数中的二维码版本
        error_correction=ERROR_CORRECTION,  # 使用参数中的纠错级别
        box_size=BOX_SIZE,  # 使用参数中的格子大小
        border=BORDER_SIZE  # 使用参数中的边框宽度
    )
    qr.add_data(data)  # 添加数据
    qr.make(fit=True)  # 自动调整二维码尺寸以适应数据

    img = qr.make_image(fill=FILL_COLOR, back_color=BACK_COLOR)  # 生成图像，使用指定的前景色和背景色
    img.save(file_name)  # 保存生成的二维码图片

# 示例：生成二维码并保存为图片
generate_qr(url, PNG)

print('二维码生成成功！！！')
