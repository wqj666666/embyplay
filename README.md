# 原理
通过nginx拦截emby播放链接，然后使用python脚本拼接alist的视频文件链接来播放。
# 使用教程
1.在nginx配置文件nginx.conf添加下面参数，拦截播放地址给脚本。我把我的nginx配置放在nginx目录里,各位可以参考配置。
```config
	#拦截emby播放地址
	location ~ ^/emby/videos/\d+/stream\.(\w+) {
    proxy_pass http://localhost:22333;
	}
```
2.在脚本修改好里面的你的alist地址和emby地址，emby用户id和emby的api。
```python
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
```
3.在embyplay脚本目录下
运行embyplay.py 
```shell
nohup python3 embyplay.py  > embyplay.log 2>&1 &

```
查看是否运行embyplay.py 
```shell
 ps ax|grep embyplay.py
```

感谢MisakaF提供的思路和Augety修改的bug，目前没有搞鉴权，需要鉴权的可以使用rclone http的方式为播放链接，再加入鉴权功能，我只是基本实现，提供一个播放分离的参考。