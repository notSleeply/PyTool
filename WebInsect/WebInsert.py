import requests # 网络请求包
from bs4 import BeautifulSoup #解析 HTML 和 XML 文档的库

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url_douban = 'https://movie.douban.com/top250'  # 这里输入你想爬取的网页
url_book = 'https://books.toscrape.com/'        # 测试用的网页

# 国外书单网址
def spider_book(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            articles = soup.find_all('article', class_='product_pod')
            with open('books.txt', 'w', encoding='utf-8') as file:
                for article in articles:
                    h3 = article.find('h3')
                    a_tag = h3.find('a')
                    title = a_tag['title']
                    p = article.find('p', class_='price_color')
                    price = p.get_text()
                    line = f"书名: {title:<100}价格:{price:<10}\n"
                    file.write(line)
                    print(line)
        print("---------------------国外书单爬取成功，内容已保存到 books.txt 文件中---------------------")
    except Exception as e:
        print("测试失败，错误信息：", e)

# 用于爬取豆瓣
def spider_douban(url):
    idx = 1
    with open('douban.txt', 'w', encoding='utf-8') as file:
        for start_num in range(0, 250, 25):
            new_url = f"{url}?start={start_num}&filter="
            response = requests.get(new_url, headers=headers)
            response.encoding = response.apparent_encoding
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                for item in soup.find_all('div', class_='item'):
                    title = item.find('span', class_='title').get_text()
                    rating = item.find('span', class_='rating_num').get_text()
                    line = f"{idx:<3}. 电影: {title:<30}评分: {rating:<5}\n"
                    file.write(line)
                    print(line)
                    idx += 1
            else:
                print("无法访问该网页, 状态码: ", response.status_code)
    print("---------------------豆瓣Top250爬取成功，内容已成功保存到douban.txt文件中---------------------")


if __name__ == '__main__':
    print("WebInsect 模块已加载，开始测试爬虫功能...")
    spider_book(url_book)  # 测试国外书单爬虫
    spider_douban(url_douban)  # 爬取豆瓣电影Top250