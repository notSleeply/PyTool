from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 抖音解析 API
DOUYIN_API = "https://api.douyin.wtf/api/hybrid/video_data?url={url}&minimal=false"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

@app.route('/parse', methods=['POST'])
def parse_video():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': '链接不能为空'}), 400

        # 打印调试信息：接收到的 URL
        print(f"Received URL: {url}")

        # 向抖音API发送请求
        response = requests.get(DOUYIN_API.format(url=url), headers=HEADERS)
        # 打印API返回的内容，查看是否正常返回数据
        print(f"Response from Douyin API: {response.text}")

        if response.status_code != 200:
            return jsonify({'error': '无法解析该链接'}), 400

        video_data = response.json()
        # 打印返回的数据结构，帮助调试
        print(f"Video Data: {video_data}")

        # 确保返回的数据结构正确
        if "data" not in video_data or "video" not in video_data["data"]:
            return jsonify({'error': '无法获取视频链接'}), 400

        video_url = video_data["data"]["video"]["download_addr"]["url_list"][0]
        title = video_data["data"].get("item_title", "video")

        return jsonify({
            'video_url': video_url,
            'title': title
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
