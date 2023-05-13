import requests
from flask import Flask, request, redirect
import random
import re
import json

from flask_cors import CORS


app = Flask(__name__)

#负载均衡的服务器,下面填写播放服务器的alist地址
play_servers = [
    "http://www.baidu.com:31003",
    "http://www.baidu.com:31002",
    "http://www.baidu.com:31001"
]
#设置权重选择，权重越大选到的概率越高
play_server_weights = [2, 3, 5]
# 更新路由以匹配多种视频格式
@app.route('/emby/videos/<int:video_id>/stream.<path:ext>')
def handle_request(video_id, ext):
    #用户id,随便一个
    userId = ""
    #emby的api
    emby_token=""
    #emby的url
    emby_url="http://127.0.0.1:8096"

    # 从 URL 中提取视频 ID 和扩展名
    match = re.search(r"/emby/videos/(\d+)/stream\.(\w+)", str(request.url))
    if match:
        video_id, ext = match.groups()

    emby_client = request.args.get("X-Emby-Client", "Emby%20Web")
    emby_device_name = request.args.get("X-Emby-Device-Name", "Chrome%20Windows")
    emby_device_id = request.args.get("X-Emby-Device-Id", "4c3bd0fd-423e-4293-946d-310662413458")
    emby_client_version = request.args.get("X-Emby-Client-Version", "4.8.0.30")
    emby_language = request.args.get("X-Emby-Language", "zh-cn")

    #获取播放信息的链接
    url = f"{emby_url}/emby/Users/{userId}/Items/{video_id}?X-Emby-Client={emby_client}&X-Emby-Device-Name={emby_device_name}&X-Emby-Device-Id={emby_device_id}&X-Emby-Client-Version={emby_client_version}&X-Emby-Token={emby_token}&X-Emby-Language={emby_language}"
   
    payload = {}
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # 获取视频路径
    SourceID = request.args["MediaSourceId"]
    data = json.loads(response.text)
    for i in data['MediaSources']:
        if i['Id'] == SourceID:
            Path = i['Path']
    # 随机选择一个播放服务器
    selected_play_server = random.choices(play_servers, weights=play_server_weights, k=1)[0]
  
    # 拼装播放链接，我这里是拼装alist的链接
    play_url = f"{selected_play_server}/p{Path}"
    print(play_url)

    # 重定向到播放服务器
    return redirect(play_url)

# 在Flask应用中启用CORS
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(port=22333, debug=True)
