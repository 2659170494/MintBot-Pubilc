# MintBot

### 两周年了，这应该是最后一次的更新了(Nonebot仍在版本开发中)
又一年了，2023年发生的是真的五味杂陈。

简要谈谈机器人的事，

go-cqhttp和oicq之类的协议机器人几乎等于停更状态了，

不使用签名的话几乎无法使用。

而且unidbg-qsign涉及安全问题，原作者已被拿下，

而现有的遗留代码也因为签名库的更新逐渐失效。

目前正在转至HOOK机器人方案。

不过因为懒癌发作的原因，这个项目迟迟没更新😂。

原机器人服务也停更了半年了。

预计这两个月完成v2的移植，并且尝试更新新的服务器。

简要说下这个项目的最低配置，

该代码运行在Windows7(2g2h)+Python3.8的环境

nonebot2勉强能跑，平台是我的免费云

说实话到2024年也能跑已经不是例外了😂

镜像仓库：[Github](https://github.com/2659170494/MintBot-Pubilc )

主仓库：[Gitee](https://gitee.com/greenyoshi233/MintBot-Pubilc )

#### 介绍
MintBot---薄荷机器人,是一个作者个人边学习边实践Python的个人作品之一(一个功能较多的自制机器人)

#### 软件架构
Python3+Go-Cqhttp


#### 安装教程

1.  需使用Python 3的PIP安装代码会用到的库，你可以在QQbOT.PY里查看。安装ffmpeg-python前请一定要看该库的官方Github站( https://github.com/kkroening/ffmpeg-python )，使用该库的"音乐搜索"功能请务必观看安装教程(该功能依赖该的是ffmpeg-python库,而不是ffmpeg或python-ffmpeg。如果您的python装有这两个库请卸载他们(不卸载会导致冲突)。使用该库请在自己的机器上安装ffmpeg))
2.  在https://go-cqhttp.org 下载Go-Cqhttp并登陆帐号，在config.yml中设置反向HTTP POST的Url为你使用MintBot的服务器和py文件中设置的反向Post端口
3.  在项目的QQBot.py中修改对应配置
4.  测试完成后即可使用(可根据自己需求修改文件)

#### 使用说明

1.  在私聊对发送"'机器人名字'，在吗"或戳一戳可确认机器人是否可以正常发送消息
2.  目前支持功能可以查看菜单列表有的，当然也有些功能并没有显示出来(可以自己去看看哇awa)
3.  可自己在代码文件中自定义功能和回复方式

#### 参与贡献

1.  Fork 本仓库
2.  新建 "YourName"_master 分支
3.  提交代码
4.  新建 Pull Request


#### 关于

1.  机器人仅供娱乐使用
2.  如有侵权可联系：13178026480@163.com

