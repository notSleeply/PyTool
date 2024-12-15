import random  # 导入生成随机数的模块
import string  # 导入字符串处理模块

# 参数部分：用户可以根据需要修改这些参数
password_length = 12  # 设置密码的长度
password_count = 5    # 设置生成密码的个数
use_uppercase = False  # 是否使用大写字母
use_lowercase = True  # 是否使用小写字母
use_digits = True     # 是否使用数字
use_punctuation = False  # 是否使用标点符号
filename = "password.txt"  # 设置保存密码的文件名

# 根据用户选择的参数，生成字符集
def get_character_set():
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_punctuation:
        characters += string.punctuation
    return characters

# 生成密码的函数
def generate_password(length=12):
    # 获取字符集
    characters = get_character_set()
    if not characters:
        raise ValueError("字符集不能为空，请至少选择一种字符类型")
    # 使用列表生成式随机选择字符并组合成密码
    # random.choice(characters)：从字符集中随机选择一个字符。
    # ''.join(...)：将生成的字符列表拼接成一个字符串。
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# 将生成的密码保存到 txt 文件中，追加到文件末尾
def save_password_to_file(passwords, filename):
    # 以追加模式打开文本文件
    with open(filename, 'a') as file:
        # 将生成的每个密码写入文件，文件末尾添加换行符
        for password in passwords:
            file.write(password + '\n')

# 生成指定数量的密码
def generate_multiple_passwords(count, length):
    passwords = [generate_password(length) for _ in range(count)]
    return passwords

# 生成多个指定长度的密码
passwords = generate_multiple_passwords(password_count, password_length)

# 将生成的密码追加保存到指定文件中
save_password_to_file(passwords, filename)

# 打印生成的密码
print("生成的密码如下:")
for password in passwords:
    print(password)