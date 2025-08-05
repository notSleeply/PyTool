import os
import re
import time
import requests
from wxauto import WeChat

# 抖音解析 API
DOUYIN_API = "https://api.douyin.wtf/api/hybrid/video_data?url={url}&minimal=false"

# 设置 User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# 监听的好友
LISTEN_FRIENDS = ["文件传输助手", "一笑"]

# 初始化微信
wx = WeChat()

# 监听好友
for friend in LISTEN_FRIENDS:
    wx.AddListenChat(who=friend)

def extract_douyin_url(text):
    """从消息文本中提取抖音短链接"""
    match = re.search(r'https?://v\.douyin\.com/\S*', text)
    return match.group(0).strip().split()[0] if match else None

def get_real_url(short_url):
    """解析抖音短链接，获取最终跳转的真实 URL"""
    try:
        response = requests.get(short_url, headers=HEADERS, allow_redirects=True)
        if response.status_code == 200:
            print(f"[✅ 解析短链接成功] {response.url}")
            return response.url
        else:
            print(f"[❌ 解析失败] 状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[❌ 解析错误] {e}")
        return None

def get_video_info(video_url):
    """调用 API 获取无水印视频信息"""
    api_url = DOUYIN_API.format(url=video_url)
    try:
        response = requests.get(api_url, headers=HEADERS)
        data = response.json()
        if data.get("code") != 200:
            print("[❌ API 解析失败]")
            return None
        return {
            "title": data["data"]["item_title"],
            "video_url": data["data"]["video"]["download_addr"]["url_list"][0],
        }
    except requests.RequestException as e:
        print(f"[❌ API 请求错误] {e}")
        return None

def sanitize_filename(filename):
    """去除非法字符"""
    return re.sub(r'[\/:*?"<>|]', "_", filename)

def download_video(video_url, title):
    """下载视频并保存为【标题】.mp4"""
    filename = sanitize_filename(title) + ".mp4"
    if os.path.exists(filename):
        print(f"[⏭️ 跳过] 文件已存在: {filename}")
        return filename
    try:
        with requests.get(video_url, headers=HEADERS, stream=True) as response:
            response.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"[✅ 下载完成] {filename}")
        return filename
    except requests.RequestException as e:
        print(f"[❌ 下载失败] {e}")
        return None

def send_video_to_wechat(friend, video_path):
    """发送视频到微信好友"""
    if os.path.exists(video_path):
        wx.SendFiles(filepath=video_path, who=friend)
        print(f"[✅ 已发送] {video_path} → {friend}")
    else:
        wx.SendMsg(msg="❌ 视频下载失败，请稍后再试", who=friend)

def process_messages():
    """监听消息并处理抖音视频下载"""
    while True:
        msgs = wx.GetListenMessage()
        for chat in msgs:
            who = chat.who  # 发送者
            messages = msgs.get(chat)
            for msg in messages:
                content = msg.content  # 消息内容
                print(f"[📩 收到消息] {who}: {content}")

                # 检查是否是抖音短链接
                short_url = extract_douyin_url(content)
                if short_url:
                    wx.SendMsg(msg="🎬 解析中，请稍等...", who=who)
                    real_url = get_real_url(short_url)
                    if real_url:
                        video_info = get_video_info(real_url)
                        if video_info:
                            wx.SendMsg(msg=f"✅ 解析成功: {video_info['title']}\n🎬 正在下载...", who=who)
                            video_path = download_video(video_info["video_url"], video_info["title"])
                            if video_path:
                                send_video_to_wechat(who, video_path)
                            else:
                                wx.SendMsg(msg="❌ 视频下载失败，请稍后再试", who=who)
                    else:
                        wx.SendMsg(msg="❌ 无法解析链接，请检查链接是否有效", who=who)
        time.sleep(1)  # 每 1 秒检测一次新消息

# 启动监听
process_messages()
