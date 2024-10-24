import requests # 网络请求包
from bs4 import BeautifulSoup #解析 HTML 和 XML 文档的库


url = 'http://freefs.net3v.club/'  # 这里输入你想爬取的网页

# 用于爬取网页内容
def simple_spider(url):
    # 发送HTTP请求获取网页内容
    response = requests.get(url)

    # 尝试从HTTP头部获取编码方式，如果未能识别则手动设置为utf-8
    response.encoding = response.apparent_encoding

    # 检查请求是否成功（状态码200表示成功）
    if response.status_code == 200:
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 打开一个txt文件，准备写入内容
        with open('output.txt', 'w', encoding='utf-8') as file:
            # 写入网页的标题
            if soup.title:
                file.write("网页标题: " + soup.title.string + '\n\n')

            # 获取网页中的所有文本内容，并去除多余的空白字符
            text = soup.get_text(separator='\n', strip=True)

            # 将文本内容写入文件
            file.write("网页文本内容:\n" + text + '\n')

        print("网页内容已成功保存到output.txt文件中")
    else:
        print("无法访问该网页, 状态码: ", response.status_code)


# 使用该函数爬取某个网页内容
simple_spider(url)