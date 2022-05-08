# MintBot

本代码因无法连接至Github(" https://github.com/2659170494/MintBot ")默认在Gitee(" https://gitee.com/GreenYoshi/MintBot ")更新,Github(" https://github.com/2659170494/MintBot ")上的代码能否更新完全看运气!!!

#### 介绍
MintBot---薄荷机器人,是一个作者个人边学习边实践Python的个人作品之一(一个功能较多的自制机器人,该版本为公开版本)

#### 软件架构
Python3+Go-Cqhttp


#### 安装教程

1.  需使用Python 3的PIP安装库:keyword，socket，json，requests，random，urllib，time，os，filetype，demjson，cmath，hashlib，base64，ffmpeg-python(V20220508以后,安装ffmpeg-python前请一定要看该库的官方Github站( https://github.com/kkroening/ffmpeg-python )，使用该库的"音乐搜索"功能请务必观看安装教程(该功能依赖该的是ffmpeg-python库,而不是ffmpeg或python-ffmpeg。如果您的python装有这两个库请卸载他们(不卸载会导致冲突)。使用该库请在自己的机器上安装ffmpeg))
2.  在https://go-cqhttp.org 下载Go-Cqhttp并登陆帐号，在config.yml中设置反向HTTP POST的Url为你使用MintBot的服务器和py文件中设置的反向Post端口
3.  在项目的QQBot.py中修改对应配置
4.  测试完成后即可使用(可根据自己需求修改文件)

#### 使用说明

1.  在私聊对机器人回复"'机器人名字'，在吗"(在群聊"@机器人,在吗")可确认机器人是否可以正常发送消息
2.  目前支持功能有：(戳一戳)"机器人名字"，(菜单，找找"名字"(搜索涂鸦宇宙图鉴)，今日早报(获取今日60秒早报)，来只毛(在绒狸API(V1)随机获取图片)，"城市"天气(调用和风天气API获取城市天气)，"音乐平台"搜歌"歌名"(调用音乐搜索器API获取音乐)，发送消息"内容"(到"号码"(人/群))(管理员可用，发送消息到指定位置)，(丢/赞/爬/摸摸)"QQ号"(发送自定义表情)，摸鱼日历(调用韩小韩API获取今日摸鱼日历))(V20220507)
3.  可自己在代码文件中自定义功能和回复方式

#### 参与贡献

1.  Fork 本仓库
2.  新建 "YourName"_master 分支
3.  提交代码
4.  新建 Pull Request


#### 关于

1.  机器人仅供娱乐使用
2.  如有侵权可联系：13178026480@163.com

