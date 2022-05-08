# -*- coding: UTF-8 -*-import receive
import base64
import socket
import json
import requests
import random
import urllib
import time
import os
import filetype
import demjson
import ffmpeg
import hashlib
from ast import Continue
from cmath import exp
from keyword import kwlist
#下面是一些配置。
QQID="" #机器人的QQ号
adminQQ = [''] #管理员QQ列表
superadmin = '' #超级管理员(机主)
weatherKEY = '' #和风天气WebAPI的KEY
onemingKey = '' #一铭API(https://api.wer.plus/)密钥
#furauthKey = '' #绒狸开源机器人KEY,若没有请联系官方获取(密钥仅V2需使用，V1不受影响)
furauthKey = '' #绒狸开源机器人KEY,若没有请联系官方获取(密钥仅V2需使用，V1不受影响)
ZlibUserEmail = '' #服务器出现问题(或者说被墙了)，暂时停止维护
ZlibPassword = '' #服务器出现问题(或者说被墙了)，暂时停止维护
cqhttpserverip = '127.0.0.1' #CQ-Http服务器地址(Go-Cqhttp)
cqhttpserveriphost = 5700 #CQ-Http服务器地址端口(Go-Cqhttp)
cqhttpposthost = 1317 #CQ-Http服务器反向Post端口
cqhttpaccesstoken = '' #连接CQ-Http服务器用的access_token，没有则留空
MintBotVersion = 'MintBot V20220508' #机器人版本号
BotName = '薄荷本兽' #机器人名字
ZlibraryURL = 'zh.book4you.org' #服务器可以链接到Zlibrary的地址(无须加 http:// 或 https:// )(检查可用链接请访问:https://zh.1lib.domains/?redirectUrl=/) #服务器出现问题(或者说被墙了)，暂时停止维护
menulist = [BotName+',找找(名字) ---在涂鸦宇宙中查找小伙伴',BotName+',今日早报 ---查看今日的60秒早报',BotName+',来只毛 ---随机在绒狸API获取一张毛图片',BotName+',(城市)天气 ---在和风天气查找对应城市的实时天气',BotName+',(音乐平台)搜歌(歌名) ---在音乐搜索器API搜索歌曲(若不知道支持平台可以把平台名字留空后发送查看)',BotName+'丢(/赞/爬/摸摸)(QQ号) ---发送自定义表情',BotName+',摸鱼日历 ---调用韩小韩API获取今日摸鱼日历',] #机器人目前支持的功能
pokelist = [' 嗷呜OwO',' 呜呜不要再戳了QwQ',' 哇啊好痛QAQ',' awa',' 喵呜OwO',' ~~'] #机器人被戳一戳后会随机发送的消息
songlist = ['网易云','QQ音乐','酷狗','酷我','千千','一听','咪咕','荔枝','蜻蜓','喜马拉雅','5sing原创','5sing翻唱','全民K歌'] #目前音乐搜索器支持的音乐平台
privateblacklist = [] #私聊黑名单
groupblacklist = [] #群聊黑名单
#上面是一些配置
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind((str(cqhttpserverip), int(cqhttpposthost)))
ListenSocket.listen(100)
HttpResponseHeader = '''HTTP/1.1 200 OK
Host: 127.0.0.1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

'''
print('机器人QQ号:'+QQID)
print('超级管理员QQ：'+str(superadmin))
print('和风天气API的KEY：'+weatherKEY)
print('一铭API密钥：'+str(onemingKey))
print('Z-library链接：'+ZlibraryURL) #服务器出现问题(或者说被墙了)，暂时停止维护
print('Z-library登录邮箱：'+ZlibUserEmail) #服务器出现问题(或者说被墙了)，暂时停止维护
print('Z-library登录密码：'+ZlibPassword) #服务器出现问题(或者说被墙了)，暂时停止维护
print('CQ-HTTP服务端IP：'+cqhttpserverip)
print('CQ-HTTP服务端IP端口：'+str(cqhttpserveriphost))
print('CQ-HTTP服务端反向Post端口：'+str(cqhttpposthost))
print('CQ-HTTP服务端access_token：' + str(cqhttpaccesstoken))
print('机器人名字：'+BotName)
print('机器人版本：'+MintBotVersion)
print('私聊黑名单:'+str(privateblacklist))
print('群聊黑名单:'+str(groupblacklist))
print('配置加载完成，若信息错误请自己修改配置信息。')
def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="\n":
            return json.loads(msg[i:])
    return None
#需要循环执行，返回值为json格式
def rev_msg():# json or None
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    rev_json=request_to_json(Request)
    #Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    messageRefresh = 1
    return rev_json
def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((str(cqhttpserverip), int(cqhttpserveriphost)))
    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息
    # 将字符中的特殊字符进行url编码
    try:
        msg = msg.replace(" ", "%20")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("\n", "%0a")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("&", "%26")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("&#91;","[")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("&#93;","]")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("%26#91;","[")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("%26#93;","]")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    if msg_type == 'group':
        if cqhttpaccesstoken != '':
            payload = "GET /send_group_msg?access_token="+str(cqhttpaccesstoken)+"&group_id=" + str(
                number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + str(cqhttpserverip) + ":"+str(cqhttpserveriphost)+"\r\nConnection: close\r\n\r\n"
        else:
            payload = "GET /send_group_msg?group_id=" + str(
                number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + str(cqhttpserverip) + ":"+str(cqhttpserveriphost)+"\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        if cqhttpaccesstoken != '':
            try:
                msg = msg.replace("[CQ:at,qq="+str(searchsongQQ)+"]", "您好")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace('[CQ:at,qq='+str(qq)+']',"您好")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:at,qq="+str(searchsongQQ)+"]","您好")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=156]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=74]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=161]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=157]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=160]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=162]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            payload = "GET /send_private_msg?access_token="+str(cqhttpaccesstoken)+"&user_id=" + str(
                number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + str(cqhttpserverip) + ":"+str(cqhttpserveriphost)+"\r\nConnection: close\r\n\r\n"
        else:
            try:
                msg = msg.replace("[CQ:at,qq="+str(searchsongQQ)+"]", "您好")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace('[CQ:at,qq='+str(qq)+']',"您好")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:at,qq="+str(searchsongQQ)+"]","您好")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=156]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=74]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=161]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=157]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=160]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            try:
                msg = msg.replace("[CQ:face,id=162]","")
                Continue
            except BaseException as error:
                #print('所有异常的基类：'+str(error))
                Continue
            payload = "GET /send_private_msg?user_id=" + str(
                number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + str(cqhttpserverip) + ":"+str(cqhttpserveriphost)+"\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0
def get_group(id):
    if cqhttpaccesstoken != '':
        response = requests.post('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_list?access_token='+str(cqhttpaccesstoken)+'&group_id='+str(id)).json()
    else:
        response = requests.post('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_list?group_id='+str(id)).json()
    for i in response['data']:
        if(i['card']!=''):
            print(i['card']+str(i['user_id']))
        else:
            print(i['nickname']+str(i['user_id']))
def sea_mp3(songpagefun):
    songaddress = 'http://www.xmsj.org/'
    songnamelist = []
    songimagelist = []
    songlinklist = []
    songmp3list = []
    songidlist = []
    messagescucess = 0
    songlistline = 0
    songpage = int(songpagefun)
    songheader = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4515.159 Safari/537.36','X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Accept':'application/json, text/javascript, */*; q=0.01','Connection':'keep-alive'}
    songdata = {'input':str(songname),'filter':'name','type':str(songtype),'page':int(songpage)}
    print(songdata)
    #songgetrequestscookies = requests.get('http://ia.51.la/go1?id=19997613').cookies
    #print(songgetrequestscookies)
    #songpostrequests = requests.post(songaddress, data=songdata,cookies=songgetrequestscookies,headers=songheader).text
    songpostrequests = requests.post(songaddress, data=songdata,headers=songheader).text
    print(songpostrequests)
    songjson = demjson.decode(songpostrequests)
    if songjson.get("code") == 200:
        songmessage = "[CQ:face,id=12]嗷呜OwO，这是搜索到的歌曲：" + str('\n')
        for songline in songjson.get("data"):
            songnamelist.append(songline.get("title")+'---'+songline.get('author'))
            print(songline.get("title")+'---'+songline.get('author'))
            songimagelist.append(songline.get("pic"))
            print(songline.get("pic"))
            songidlist.append(songline.get("songid"))
            print(songline.get("songid"))
            songlinklist.append(songline.get("link"))
            print(songline.get("link"))
            songmp3list.append(songline.get("url"))
            print(songline.get("url"))
            songmessage = songmessage + '歌名：'+ str(songline.get("title"))+'---'+str(songline.get('author')) + str("\n") + '歌曲ID：'+ str(songline.get("songid")) + str("\n") + '[CQ:image,file='+str(songline.get("pic"))+']'+str("\n") + '歌曲链接：' + str(songline.get("link")) + str("\n")
            songlistline = songlistline +1
            print(songlistline)
        songmessage = songmessage + str('"音乐API来自音乐搜索器,请根据对应序号回复对应阿拉伯数字.当前为第'+str(songpage)+'页，你可以回复"'+BotName+'，下一页"进行翻页操作(你有1分钟的操作时间,在此期间其他人无法进行操作,除非使用人执行"停止"命令或超时(任何人都可以回复"'+BotName+'，停止操作"中止执行人操作))(音乐是语音与Mp3链接一起发出，若没有受到语音可直接点击Mp3链接进行在线试听)(不支持购买播放和一份中试听，这一类的歌曲会导致语音和mp3链接一起失效)。"'+str('\n')+"-------------------"+str('\n')+MintBotVersion)
        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':songmessage})
        return 200
    elif songjson.get("code") == 404:
        print(songjson.get("error"))
        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,找不到对应的歌曲QAQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
        return 404
    else:
        print(songjson.get("error"))
        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(songjson.get("error"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
        return songjson.get("code")
def furbotbuildSignString(apiPath,timestamp,authKey):
    #timestamp = int(time.time())
    furoriginal = int(str(apiPath)+'-'+str(timestamp)+'-'+str(authKey))
    print(furoriginal)
    furhash = int(hashlib.md5())
    print(furhash)
    #furoriginal = bytearray(furoriginal)
    #furhash.update(furoriginal.encode("utf-8"))
    #base64data=base64.b64encode(furhash.digest()).decode('utf-8')
    #funbyte = int(bytes("".join(map(str,furhash.digest(bytearray(furoriginal))))), base=16)
    funbytearray = bytearray(furoriginal, 'utf-8')
    print(funbytearray)
    furhash.update(funbytearray)
    funhashdigest = furhash.digest()
    print(funhashdigest)
    funbytes = bytes(funhashdigest)
    print(funbytes)
    #fun16byte = int(str(funbytes),base=16)
    #fun16byte = hex(ord(funbytes))
    fun16byte = hex(funbytes)
    print(fun16byte)
    if fun16byte == '' or fun16byte == 'null':
        if len(fun16byte) > 1:
            funreturn =int(bytes("".join(map(fun16byte))))
            print(funreturn)
        else:
            funreturn = int(bytes("".join(map('0' + str(fun16byte)))))
            print(funreturn)
    else:
        funreturn =int(bytes("".join(map(fun16byte))))
        print(funreturn)
    #funreturn = funbyte
    return funreturn
    
print('接受端口为'+str(cqhttpposthost)+'，请自行在Bot服务端中设置反向HTTP POST地址。')
Zliblogin = 0
print('加载完毕，欢迎使用MintBot!')
while True:
    try:
        rev = rev_msg()
        print(rev)
        if rev == None:
            continue
    except:
        continue
    if rev["post_type"] == "message":
        #print(rev) #需要功能自己DIY
        try:
            #if rev["message_type"] == "private": #私聊
                #message = rev["raw_message"]
                #qq = rev['sender']['user_id']
                #wmsucessful =1
                #print('消息为私聊类')
                #if message=='在吗':
                    #send_msg({'msg_type':'private','number':qq,'msg':'嗷呜~~我在'+str('\n')+"-------------------"+str('\n')+MintBotVersion})
            #elif rev["message_type"] == "group" or rev["message_type"] == "private": #群聊
            if rev["message_type"] == "group" or rev["message_type"] == "private": #群聊和私聊
                if rev["message_type"] == "group":
                    sendid = rev['group_id']
                    message = rev["raw_message"]
                    qq=rev['sender']['user_id']
                    messagetype = 'group'
                    wmsucessful = 1
                if rev["message_type"] == "private":
                    sendid = rev['sender']['user_id']
                    message = rev["raw_message"]
                    qq = rev['sender']['user_id']
                    messagetype = 'private'
                    try:
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'收到来自'+str(sendid)+'的消息：'+str(message)})
                        Continue
                    except BaseException as error:
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'收到消息但发送了错误QAQ：'+str(error)})
                        Continue
                    wmsucessful =1
                #print('消息为群消息类')
                print('消息为群聊和私聊消息类')
                if qq in privateblacklist or qq in groupblacklist or sendid in privateblacklist or sendid in groupblacklist:
                    try:
                        send_msg({'msg_type':'private','number':int(superadmin),'msg':'收到来自'+str(sendid)+'(在黑名单内)的'+str(messagetype)+'消息：'+str(message)})
                        Continue
                    except BaseException as error:
                        send_msg({'msg_type':'private','number':int(superadmin),'msg':'收到'+str(messagetype)+'消息但发送了错误QAQ：'+str(error)})
                        Continue
                    message = ""
                if "[CQ:at,qq="+QQID+"]" in message:
                    if rev['raw_message'][len(rev['raw_message'])-2:len(rev['raw_message'])]=='在吗':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:poke,qq={}]'.format(qq)})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:face,id=147]'})
                if message[0:len(BotName)+1] == BotName+',' or message[0:len(BotName)+1] == BotName+'，' or message[0:len("[CQ:at,qq="+QQID+"]")+2] == "[CQ:at,qq="+QQID+"] "+"，" or message[0:len("[CQ:at,qq="+QQID+"]")+2] == "[CQ:at,qq="+QQID+"] "+","or message[0:len("[CQ:at,qq="+QQID+"]")+1] == "[CQ:at,qq="+QQID+"]"+"，" or message[0:len("[CQ:at,qq="+QQID+"]")+1] == "[CQ:at,qq="+QQID+"]"+",":
                    if message[0:len("[CQ:at,qq="+QQID+"]")+1] == "[CQ:at,qq="+QQID+"] ":
                        messagecommand = message[len("[CQ:at,qq="+QQID+"]")+2:len(message)]
                    elif message[0:len("[CQ:at,qq="+QQID+"]")] == "[CQ:at,qq="+QQID+"]":
                        messagecommand = message[len("[CQ:at,qq="+QQID+"]")+1:len(message)]
                    else:
                        messagecommand = message[len(BotName)+1:len(message)]
                    print(messagecommand)
                    if  messagecommand[0:2] == "找找":
                        findfriend = messagecommand[2:len(messagecommand)]
                        findfriendurl = 'https://duo-api.turka.cn/tuyafriends/?name='
                        findfriendrequests = requests.get(findfriendurl+urllib.parse.quote(findfriend)).text
                        findfriendjson = demjson.decode(findfriendrequests)
                        if findfriendjson.get("code") == 200:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=147]"+str(findfriendjson.get('data').get('name'))+'（ID：'+str(findfriendjson.get('data').get('id'))+'）'+str('\n')+"[CQ:face,id=144]破壳："+str(findfriendjson.get('data').get('birthday'))+str('\n')+"[CQ:face,id=75]家乡："+str(findfriendjson.get('data').get("hometown"))+str('\n')+"[CQ:face,id=159]物种："+str(findfriendjson.get('data').get("animal"))+str('\n')+"[CQ:face,id=12]性格："+str(findfriendjson.get('data').get("character"))+str('\n')+"[CQ:face,id=66]喜欢："+str(findfriendjson.get('data').get("likes"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(findfriendjson.get('data').get("intro"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=https://duo-api.turka.cn/tuyafriends/img/"+str(findfriendjson.get('data').get('imgid'))+".png]"})
                        elif findfriendjson.get("code") == -10:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=106]呜呜，我好像没有找到他呢，该不会是没来过？QwQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+findfriendjson.get("code")+"):"+findfriendjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    #elif message[0:7] == "涂鸦宇宙,找找" or message[0:7] == "涂鸦宇宙，找找":
                        #if 14<=int(time.strftime("%H"))<=16:
                            #continue
                        #else:
                            #findfriend = message[7:len(message)]
                            #findfriendurl = 'https://duo-api.turka.cn/tuyafriends/?name='
                            #findfriendrequests = requests.get(findfriendurl+urllib.parse.quote(findfriend)).text
                            #findfriendjson = json.loads(findfriendrequests)
                            #if findfriendjson.get("code") == 200:
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=147]"+str(findfriendjson.get('data').get('name'))+'（ID：'+str(findfriendjson.get('data').get('id'))+'）'+str('\n')+"[CQ:face,id=144]破壳："+str(findfriendjson.get('data').get('birthday'))+str('\n')+"[CQ:face,id=75]家乡："+str(findfriendjson.get('data').get("hometown"))+str('\n')+"[CQ:face,id=159]物种："+str(findfriendjson.get('data').get("animal"))+str('\n')+"[CQ:face,id=12]性格："+str(findfriendjson.get('data').get("character"))+str('\n')+"[CQ:face,id=66]喜欢："+str(findfriendjson.get('data').get("likes"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(findfriendjson.get('data').get("intro"))})
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=https://duo-api.turka.cn/tuyafriends/img/"+str(findfriendjson.get('data').get('imgid'))+".png]"})
                            #elif findfriendjson.get("code") == -10:
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=106]呜呜，我好像没有找到他呢，该不会是没来过？"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            #else:
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+findfriendjson.get("code")+"):"+findfriendjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    #elif message[0:9] == "涂鸦宇宙，今日早报" or message[0:9] == "涂鸦宇宙,今日早报":
                        #if 14<=int(time.strftime("%H"))<=16:
                            #continue
                        #else:
                            #sixtysurl = 'https://api.03c3.cn/zb/api.php'
                            #sixtysrequests = requests.get(sixtysurl).text
                            #sixtysjson = json.loads(sixtysrequests)
                            #if sixtysjson.get("code") == 200:
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜,这是今天的早报"+str('\n')+"[CQ:image,file="+str(sixtysjson.get('imageUrl'))+str('\n')+"当前早报的时间:"+sixtysjson.get("datatime")+"."+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            #else:
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+sixtysjson.get("code")+"):"+sixtysjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif  messagecommand[0:4] == "今日早报":
                        sixtysurl = 'https://api.03c3.cn/zb/api.php'
                        sixtysrequests = requests.get(sixtysurl).text
                        sixtysjson = json.loads(sixtysrequests)
                        if sixtysjson.get("code") == 200:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜,这是今天的早报"+str('\n')+"[CQ:image,file="+str(sixtysjson.get('imageUrl'))+"]"+str('\n')+"当前早报的时间:"+sixtysjson.get("datatime")+"."+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+sixtysjson.get("code")+"):"+sixtysjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif  messagecommand[0:3] == "来只毛":
                        microtailurl = 'https://api.tail.icu/'
                        if furauthKey == '':
                            microtailurl = microtailurl+'api/v1/getFursuit/json'
                            microtailrequests = requests.get(microtailurl).text
                            microtailjson = json.loads(microtailrequests)
                            if microtailjson.get("code") == 200:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜！有请毛毛："+str(microtailjson.get("data").get("name"))+"（ID："+str(microtailjson.get("data").get("id"))+"）"+str("\n")+"内容来自：绒狸MicroTail"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                                microtailimg = requests.get(microtailjson.get('data').get("url"))
                                microtailfiletype = filetype.guess(microtailimg.content)
                                print(microtailimg)
                                with open(os.getcwd()+"\microtailtmp."+microtailfiletype.extension,'wb') as f:
                                    f.write(microtailimg.content)
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\microtailtmp."+microtailfiletype.extension+"]"})
                            else:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+microtailjson.get("code")+")："+microtailjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            Continue
                    #elif message[0:8] == "涂鸦宇宙，来只毛" or message[0:8] == "涂鸦宇宙,来只毛" :
                        #if 14<=int(time.strftime("%H"))<=16:
                            #continue
                        #else:
                            #microtailurl = 'https://api.tail.icu/api/v1/getFursuit/json'
                            #microtailrequests = requests.get(microtailurl).text
                            #microtailjson = json.loads(microtailrequests)
                            #if microtailjson.get("code") == 200:
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜！有请毛毛："+str(microtailjson.get("data").get("name"))+"（ID："+str(microtailjson.get("data").get("id"))+str("\n")+"）内容来自：绒狸MicroTail"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                #os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                                #microtailimg = requests.get(microtailjson.get('data').get("url"))
                                #microtailfiletype = filetype.guess(microtailimg.content)
                                #print(microtailimg)
                                #with open(os.getcwd()+"\microtailtmp."+microtailfiletype.extension,'wb') as f:
                                    #f.write(microtailimg.content)
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\microtailtmp."+microtailfiletype.extension+"]"})
                            #else:
                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+microtailjson.get("code")+")："+microtailjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})    
                    elif messagecommand[len(messagecommand)-2:len(messagecommand)] == "天气":
                        searchweatherQQ = qq
                        searchweatherurl = "https://geoapi.qweather.com/v2/city/lookup?key="+weatherKEY+'&location='
                        searchweatherrequests = requests.get(searchweatherurl+messagecommand[0:len(messagecommand)-2]).text
                        searchweatherjson = json.loads(searchweatherrequests)
                        if searchweatherjson.get("code") == '200':
                            searchweatherlist = searchweatherjson.get("location")
                            swlistlen = 0
                            swmessage = str('')
                            swlistID = []
                            swlistName = []
                            print(searchweatherlist)
                            if len(searchweatherlist) == 1:
                                print('OK')
                                for swlen in searchweatherlist:
                                    swjson = swlen
                                    print('OK')
                                    break
                                swname = swjson.get("name")
                                swid = swjson.get("id")
                                weatherurl = "https://devapi.qweather.com/v7/weather/now?key="+weatherKEY+"&location="
                                weatherrequests = requests.get(weatherurl+swid).text
                                weatherjson = json.loads(weatherrequests)
                                if weatherjson.get("code") == '200':
                                    wtime = weatherjson.get("updateTime")
                                    wjson = weatherjson.get("now")
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:face,id=12]嗷呜，今天'+str(swname)+'天气：'+str('\n')+'[CQ:face,id=156]天气：'+str(wjson.get("text"))+str("\n")+'[CQ:face,id=74]温度：'+str(wjson.get("temp"))+str('\n')+'[CQ:face,id=74]体感温度：'+str(wjson.get("feelsLike"))+str("\n")+'[CQ:face,id=161]风向：'+str(wjson.get("windDir"))+str("\n")+'[CQ:face,id=161]风向360角度：'+str(wjson.get("wind360"))+str("\n")+'[CQ:face,id=161]风力等级：'+str(wjson.get('windScale'))+str('\n')+'[CQ:face,id=161]风速：'+str(wjson.get('windSpeed'))+str('\n')+'[CQ:face,id=161]大气气压：'+str(wjson.get('pressure'))+str('\n')+'[CQ:face,id=157]当前小时累计降水量：'+str(wjson.get('precip'))+str('\n')+'[CQ:face,id=157]相对湿度：'+str(wjson.get('humidity'))+str('\n')+'[CQ:face,id=157]露点温度：'+str(wjson.get('dew'))+str('\n')+'[CQ:face,id=156]云量：'+str(wjson.get('cloud'))+str('\n')+'[CQ:face,id=160]能见度：'+str(wjson.get('vis'))+str('\n')+'[CQ:face,id=162]当前天气API最新时间：'+str(wtime)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                    continue
                                else:
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+weatherjson.get("code")+")"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                    continue
                            else:
                                while swlistlen != len(searchweatherlist)+1:
                                    try:
                                        if swlistlen != len(searchweatherlist):
                                            for swlen in searchweatherlist:
                                                print(swlistlen)
                                                swjson = swlen
                                                print(swlen)
                                                swmessage = swmessage +str(swlistlen) + '：' + str(swjson.get("adm1")) + "，" + str(swjson.get("adm2")) + "，" + str(swjson.get("name")) + "(ID：" + str(swjson.get("id")) + ")" +'\n' + '+'
                                                swlistlen = swlistlen + 1
                                                swlistID.append(swjson.get("id"))
                                                swlistName.append(swjson.get("name"))
                                            swmessage = swmessage + str('"天气API来自和风天气,请根据对应序号回复对应阿拉伯数字(在此期间其他人无法进行操作(任何人都可以回复"'+BotName+'，停止操作"中止执行人操作))。"'+str('\n')+"-------------------"+str('\n')+MintBotVersion)
                                            print(swlistlen)
                                            send_msg({"msg_type":str(messagetype),"number":sendid,"msg":"[CQ:face,id=12]嗷呜，这是搜索到的天气OwO："+str("\n")+str(swmessage)})
                                        else:
                                            print("开始等待回复...")
                                            print(swlistID)
                                            print(swlistName)
                                            print(searchweatherQQ)
                                            wmsucessful = 0
                                            messageRefresh = 0
                                            while wmsucessful == 0:
                                                    if True:
                                                        rev = rev_msg()
                                                        print(rev)
                                                        if rev == None:
                                                            continue
                                                        if rev["post_type"] == "message":
                                                                if rev["message_type"] == "group" or rev["message_type"] == "private": #群聊和私聊
                                                                    if rev["message_type"] == "private": 
                                                                        sendid = rev['sender']['user_id']
                                                                        message = rev["raw_message"]
                                                                        qq = rev['sender']['user_id']
                                                                        messagetype = 'private'
                                                                    elif rev["message_type"] == "group":             
                                                                        sendid = rev['group_id']
                                                                        message = rev["raw_message"]
                                                                        qq=rev['sender']['user_id']
                                                                        messagetype = 'group'
                                                                    if qq == searchweatherQQ:
                                                                        if message.isdigit() == True:
                                                                            if int(message) <= int(swlistlen)-1:
                                                                                swname = swlistName[int(message)]
                                                                                swid = swlistID[int(message)]
                                                                                print(swname)
                                                                                print(swid)
                                                                                weatherurl = "https://devapi.qweather.com/v7/weather/now?key="+weatherKEY+"&location="
                                                                                print(weatherurl+swid)
                                                                                weatherrequests = requests.get(weatherurl+swid).text
                                                                                print(weatherrequests)
                                                                                weatherjson = json.loads(weatherrequests)
                                                                                if weatherjson.get("code") == '200':
                                                                                    wtime = weatherjson.get("updateTime")
                                                                                    wjson = weatherjson.get("now")
                                                                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:face,id=12]嗷呜，今天'+str(swname)+'天气：'+str('\n')+'[CQ:face,id=156]天气：'+str(wjson.get("text"))+str("\n")+'[CQ:face,id=74]温度：'+str(wjson.get("temp"))+str('\n')+'[CQ:face,id=74]体感温度：'+str(wjson.get("feelsLike"))+str("\n")+'[CQ:face,id=161]风向：'+str(wjson.get("windDir"))+str("\n")+'[CQ:face,id=161]风向360角度：'+str(wjson.get("wind360"))+str("\n")+'[CQ:face,id=161]风力等级：'+str(wjson.get('windScale'))+str('\n')+'[CQ:face,id=161]风速：'+str(wjson.get('windSpeed'))+str('\n')+'[CQ:face,id=161]大气气压：'+str(wjson.get('pressure'))+str('\n')+'[CQ:face,id=157]当前小时累计降水量：'+str(wjson.get('precip'))+str('\n')+'[CQ:face,id=157]相对湿度：'+str(wjson.get('humidity'))+str('\n')+'[CQ:face,id=157]露点温度：'+str(wjson.get('dew'))+str('\n')+'[CQ:face,id=156]云量：'+str(wjson.get('cloud'))+str('\n')+'[CQ:face,id=160]能见度：'+str(wjson.get('vis'))+str('\n')+'[CQ:face,id=162]当前天气API最新时间：'+str(wtime)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                                    wmsucessful = 1
                                                                                    messageRefresh = 0
                                                                                    swlistlen= swlistlen+1
                                                                                    break
                                                                                else:
                                                                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+weatherjson.get("code")+")"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                                    wmsucessful = 1
                                                                                    swlistlen=swlistlen+1
                                                                                    messageRefresh = 0
                                                                                    break
                                                                            else:
                                                                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜，数值不对,已自动取消操作QAQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                                wmsucessful = 1
                                                                                swlistlen=swlistlen+1
                                                                                messageRefresh = 0
                                                                                break    
                                                                        elif message[0:len(BotName)+5] == BotName+"，停止操作" or message[0:len(BotName)+5] == BotName+",停止操作":
                                                                            swlistlen=swlistlen+1
                                                                            print(str(searchweatherQQ)+"已中止")
                                                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchweatherQQ)+"][CQ:face,id=9]呜呜,指令已被终止qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                            wmsucessful = 1
                                                                            break
                                                                        else:
                                                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜，数值不对,已自动取消操作QAQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                            wmsucessful = 1
                                                                            swlistlen=swlistlen+1
                                                                            messageRefresh = 0
                                                                            break
                                                                    elif BotName in message:
                                                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,目前服务被"+searchweatherQQ+"占用中qwq(任何人都可以回复'"+BotName+"，停止操作'中止执行人操作)"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                        messageRefresh = 0
                                                                        continue
                                                                    #elif '涂鸦宇宙' in message:
                                                                        #if 14<=int(time.strftime("%H"))<=16:
                                                                            #messageRefresh = 0
                                                                            #continue
                                                                            #else:
                                                                            #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,目前服务被"+searchweatherQQ+"占用中qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                            #messageRefresh = 0
                                                                            #continue
                                                                    #elif wwaittime == 1:
                                                                        #swlistlen=swlistlen+1
                                                                        #print(str(searchweatherQQ)+"已超时")
                                                                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchweatherQQ)+"][CQ:face,id=9]呜呜,指令已超时qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                        #wmsucessful = 1
                                                                        #break
                                                                    elif message[0:len(BotName)+5] == BotName+"，停止操作" or message[0:9] == BotName+",停止操作":
                                                                        swlistlen=swlistlen+1
                                                                        print(str(searchweatherQQ)+"已中止")
                                                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchweatherQQ)+"][CQ:face,id=9]呜呜,指令已被终止qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                        wmsucessful = 1
                                                                        break
                                                                    else:
                                                                        continue
                                            print('循环回复已结束')
                                            break
                                    except Exception as error:
                                        print(error)
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,出错了QAQ:"+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                        break
                        elif searchweatherjson.get("code") == '404':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,没有找到这个城市qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+searchweatherjson.get("code")+")"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif messagecommand == '菜单' or messagecommand == '':
                        print('收到菜单指令')
                        menumessage = '[CQ:face,id=12]嗷呜，欢迎使用'+BotName+'机器人，这是我可以做的事情OwO：'
                        for menulistline in menulist:
                            menumessage = menumessage + str("\n")+'[CQ:face,id=161]'+menulistline
                        menumessage = menumessage + str("\n")+"-------------------"+str("\n")+MintBotVersion
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':menumessage})
                    elif messagecommand[0:2] == '找书':
                        bookname = messagecommand[2:len(messagecommand)]
                        Zlibheader = {'Host':str(ZlibraryURL),'source':'android','accept-encoding':'gzip','user-agent':'okhttp/3.12.13'}
                        if json.loads(requests.get('https://'+str(ZlibraryURL)+'/eapi/info/ok',headers=Zlibheader).text).get("success") == 1:
                            try:
                                while Zliblogin != 0:
                                    if Zliblogin == 0:
                                        Zlibloginurl = 'https://'+str(ZlibraryURL)+'/eapi/user/login'
                                        Zliblogindata = {'email':ZlibUserEmail,'password':ZlibPassword}
                                        Zlibloginrequests = requests.post(Zlibloginurl,data=Zliblogindata,headers=Zlibheader)
                                        Zlibloginrequeststext = Zlibloginrequests.text
                                        Zlibloginjson = json.loads(Zlibloginrequeststext)
                                        print(Zlibloginjson)
                                        if Zlibloginjson.get('success') == 1:   
                                            Zliblogincookies = Zlibloginrequests.cookies
                                            print(Zliblogincookies)
                                            ZlibUser = Zlibloginjson.get('user')
                                            print(ZlibUser)
                                            ZlibUsername = ZlibUser.get('name')
                                            print(ZlibUsername)
                                            ZlibUserID = ZlibUser.get('id')
                                            print(ZlibUserID)
                                            ZlibUserkey = ZlibUser.get('remix_userkey')
                                            print(ZlibUserkey)
                                            Zliblogin = 1
                                            break
                                        else:
                                            print('登录失败：'+str(Zlibloginjson))
                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,登录失败QAQ:"+str(Zlibloginjson)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                            Zliblogin = 2
                                            break
                                    else:
                                        break
                                if Zliblogin == 1:
                                    booksearchurl = 'https://'+str(ZlibraryURL)+'/eapi/book/search'
                                    booksearchdata = {"message":str(bookname),"languages"+"[]":"","extensions"+"[]":"","order":"popular"}
                                    print(json.dumps(booksearchdata))
                                    booksearchrequests = requests.post(booksearchurl,data=json.dumps(booksearchdata)).text
                                    booksearchlistjson = json.loads(booksearchrequests).get("books")
                                    booksearchlist = []
                                    booksearchIDlist = []
                                    booksearchnamelist = []
                                    print(bookname)
                                    for bsline in booksearchlistjson:
                                        booksearchlist.append(bsline)
                                        print(bsline)
                                        booksearchIDlist.append(bsline.get("id"))
                                        print(bsline.get("id"))
                                        booksearchnamelist.append(bsline.get("title"))
                                        print(bsline.get("title"))
                                elif Zliblogin == 2:
                                    Zliblogin = 0
                                else:
                                    print('登录失败：未知错误')
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,登录失败QAQ:未知错误"++str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                    Zliblogin = 0
                            except:
                                print('失败')
                        else:
                            print('连接服务器失败')
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,无法链接到服务器QAQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif '搜歌' in messagecommand:
                        if messagecommand[0:3] == '网易云' or messagecommand[0:4] == 'QQ音乐' or messagecommand[0:2] == '酷狗' or messagecommand[0:2] == '酷我' or messagecommand[0:2] == '千千' or messagecommand[0:2] == '一听' or messagecommand[0:2] == '咪咕' or messagecommand[0:2] == '荔枝' or messagecommand[0:2] == '蜻蜓' or messagecommand[0:4] == '喜马拉雅' or messagecommand[0:7] == '5sing原创' or messagecommand[0:7] == '5sing翻唱' or messagecommand[0:4] == '全民K歌' or messagecommand[0:4] == '全民k歌' or messagecommand[0:4] == 'qq音乐':
                            searchsongQQ = qq
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"]已收到搜索请求，请等待十几秒时间（在此期间无法使用其它命令，机器人回复也会变慢。若一直没有收到消息，这时候可能被封控了。解决方法可以尝试回复1~10序号猜歌(歌曲顺序按照该平台的热门程度排序)，也可以回复'"+BotName+"，停止操作'中止操作后再试一次）"})
                            if messagecommand[0:3] == '网易云':
                                songtype = 'netease'
                                songname = messagecommand[5:len(messagecommand)]
                            elif messagecommand[0:4] == 'QQ音乐' or messagecommand[0:4] == 'qq音乐':
                                songtype = 'qq'
                                songname = messagecommand[6:len(messagecommand)]
                            elif messagecommand[0:2] == '酷狗':
                                songtype = 'kugou'
                                songname = messagecommand[4:len(messagecommand)]
                            elif messagecommand[0:2] == '酷我':
                                songtype = 'kuwo'
                                songname = messagecommand[4:len(messagecommand)]
                            elif messagecommand[0:2] == '千千':
                                songtype = 'baidu'
                                songname = messagecommand[4:len(messagecommand)]
                            elif messagecommand[0:2] == '一听':
                                songtype = '1ting'
                                songname = messagecommand[4:len(messagecommand)]
                            elif messagecommand[0:2] == '咪咕':
                                songtype = 'migu'
                                songname = messagecommand[4:len(messagecommand)]
                            elif messagecommand[0:2] == '荔枝':
                                songtype = 'lizhi'
                                songname = messagecommand[4:len(messagecommand)]
                            elif messagecommand[0:2] == '蜻蜓':
                                songtype = 'qingting'
                                songname = messagecommand[4:len(messagecommand)]
                            elif messagecommand[0:4] == '喜马拉雅':
                                songtype = 'ximalaya'
                                songname = messagecommand[6:len(messagecommand)]
                            elif messagecommand[0:7] == '5sing原创':
                                songtype = '5singyc'
                                songname = messagecommand[7:len(messagecommand)]
                            elif messagecommand[0:7] == '5sing翻唱':
                                songtype = '5singfc'
                                songname = messagecommand[7:len(messagecommand)]
                            elif messagecommand[0:4] == '全民K歌' or messagecommand[0:4] == '全民k歌':
                                songtype = 'kg'
                                songname = messagecommand[6:len(messagecommand)]
                            songaddress = 'http://www.xmsj.org/'
                            songnamelist = []
                            songimagelist = []
                            songlinklist = []
                            songmp3list = []
                            songidlist = []
                            messagescucess = 0
                            songlistline = 0
                            songpage = 1
                            songheader = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4515.159 Safari/537.36','X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Accept':'application/json, text/javascript, */*; q=0.01'}
                            songdata = {'input':str(songname),'filter':'name','type':str(songtype),'page':int(songpage)}
                            print(songdata)
                            #songgetrequestscookies = requests.get('http://ia.51.la/go1?id=19997613').cookies
                            #print(songgetrequestscookies)
                            #songpostrequests = requests.post(songaddress, data=songdata,cookies=songgetrequestscookies,headers=songheader).text
                            songpostrequests = requests.post(songaddress, data=songdata,headers=songheader).text
                            print(songpostrequests)
                            songjson = demjson.decode(songpostrequests)
                            if songjson.get("code") == 200:
                                songmessage = "[CQ:face,id=12]嗷呜OwO，这是搜索到的歌曲：" + str('\n')
                                for songline in songjson.get("data"):
                                    songlistline = songlistline +1
                                    songnamelist.append(songline.get("title")+'---'+songline.get('author'))
                                    print(songline.get("title")+'---'+songline.get('author'))
                                    songimagelist.append(songline.get("pic"))
                                    print(songline.get("pic"))
                                    songidlist.append(songline.get("songid"))
                                    print(songline.get("songid"))
                                    songlinklist.append(songline.get("link"))
                                    print(songline.get("link"))
                                    songmp3list.append(songline.get("url"))
                                    print(songline.get("url"))
                                    songmessage = songmessage + '（'+str(songlistline)+'）歌名：'+ str(songline.get("title"))+'---'+str(songline.get('author')) + str("\n") + '[CQ:image,file='+str(songline.get("pic"))+']'+ str("\n")
                                    print(songlistline)
                                songmessage = songmessage + str('"音乐API来自音乐搜索器(www.xmsj.org),请根据对应序号回复对应阿拉伯数字.当前为第'+str(songpage)+'页，你可以回复"'+BotName+'，下一页(或上一页)"进行翻页操作(在此期间其他人无法进行操作(任何人都可以回复"'+BotName+'，停止操作"中止执行人操作))(不支持购买播放和一分钟试听，这一类的歌曲会导致语音和mp3链接一起失效)。"'+str('\n')+"------------------------------"+str('\n')+MintBotVersion)
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':songmessage})
                                messageRefresh = 0
                                while  messagescucess != 1:
                                    rev = rev_msg()
                                    print(rev)
                                    if rev == None:
                                        continue
                                    if rev["post_type"] == "message":
                                        #print(rev) #需要功能自己DIY
                                        try:
                                            if rev["message_type"] == "group" or rev["message_type"] == "private": #群聊和私聊
                                                if rev["message_type"] == "private": 
                                                    sendid = rev['sender']['user_id']
                                                    message = rev["raw_message"]
                                                    qq = rev['sender']['user_id']
                                                    messagetype = 'private'
                                                elif rev["message_type"] == "group":             
                                                    sendid = rev['group_id']
                                                    message = rev["raw_message"]
                                                    qq=rev['sender']['user_id']
                                                    messagetype = 'group'
                                                print('200')
                                                messageRefresh = 1
                                                if messageRefresh == 1:
                                                    if qq == searchsongQQ:
                                                        if message.isdigit() == True:
                                                            if 0 < int(message) <= int(songlistline):
                                                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜OwO，这是歌曲的一些信息:"+str("\n") +'[CQ:image,file='+str(songimagelist[int(message)-1])+']' + str("\n")+'歌名：'+ str(songnamelist[int(message)-1])+str("\n") + '歌曲ID：'+ str(songidlist[int(message)-1]) + str("\n")+'歌曲链接：' + str(songlinklist[int(message)-1]) +str("\n") + "Mp3链接："+str(songmp3list[int(message)-1])+str("\n")+"（如果不出意外地话待会会有个语音，那就是您想要的音乐了。敬请享受吧OwO。（音乐是语音与Mp3链接一起发出，若没有收到语音可直接点击Mp3链接进行在线试听））"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                messageRefresh = 0
                                                                messagescucess = 1
                                                                os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                                                                songfile = requests.get(songmp3list[int(message)-1])
                                                                if messagecommand[0:4] == 'QQ音乐':
                                                                    songfiletype = 'm4a'
                                                                    print("平台为QQ音乐，已自动设置文件类型为m4a")
                                                                else:
                                                                    songfiletype = filetype.guess(songfile.content).extension
                                                                print(songfile)
                                                                with open(os.getcwd()+"\songfiletmp."+songfiletype,'wb') as f:
                                                                    f.write(songfile.content)
                                                                if messagecommand[0:4] == 'QQ音乐':
                                                                    print("检测到特定格式，开始转换文件")
                                                                    try:
                                                                        ffmpegputaddress = str("songfiletmp."+songfiletype)
                                                                        stream = ffmpeg.input(ffmpegputaddress)
                                                                        print(stream)
                                                                        print("传入特定文件:"+str(stream))
                                                                        #stream = ffmpeg.hflip(stream)
                                                                        #stream = ffmpeg.filter(stream,'-y')
                                                                        ffmpeggetaddress = str("songfiletmp.mp3")
                                                                        stream = ffmpeg.output(stream, ffmpeggetaddress)
                                                                        print(stream)
                                                                        print("设置传出文件:"+str(stream))
                                                                        stream = ffmpeg.overwrite_output(stream)
                                                                        print(stream)
                                                                        print("设置参数:"+str(stream)) 
                                                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"]正在处理音频ing..."})
                                                                        print("开始转换")
                                                                        ffmpeg.run(stream)
                                                                        songfiletype = 'mp3'
                                                                        print("转换成功")
                                                                    except BaseException as error:
                                                                        print('转换失败，所有异常的基类：'+str(error))
                                                                        continue 
                                                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:record,file=file:///"+os.getcwd()+"\songfiletmp."+songfiletype+"]"})
                                                                break
                                                            else:
                                                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜，数值不对,已自动取消操作QAQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                messagescucess = 1
                                                                messageRefresh = 0
                                                                break
                                                        elif message[0:len(BotName)+5] == BotName+"，停止操作" or message[0:len(BotName)+5] == BotName+",停止操作":
                                                            print(str(searchsongQQ)+"已中止")
                                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,指令已被终止qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                            messagescucess = 1
                                                            messageRefresh = 0 
                                                            break
                                                        elif message[0:len(BotName)+4] == BotName+"，下一页" or message[0:len(BotName)+4] == BotName+",下一页":
                                                            songpage = songpage + 1
                                                            sea_mp3(songpage)
                                                            if sea_mp3() != '200':
                                                                break
                                                            messageRefresh = 0
                                                            continue
                                                        elif message[0:len(BotName)+4] == BotName+"，上一页" or message[0:len(BotName)+4] == BotName+",上一页":
                                                            songpage = songpage - 1
                                                            sea_mp3(songpage)
                                                            if sea_mp3() != '200':
                                                                break
                                                            messageRefresh = 0
                                                            continue
                                                        else:
                                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜，数值不对,已自动取消操作QAQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                            messagescucess = 1
                                                            messageRefresh = 0
                                                            break
                                                    elif BotName in message:
                                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,目前服务被"+searchsongQQ+"占用中qwq(任何人都可以回复'"+BotName+"，停止操作'中止执行人操作)"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                        messageRefresh = 0
                                                        continue
                                                    elif message[0:len(BotName)+5] == BotName+"，停止操作" or message[0:9] == BotName+",停止操作":
                                                        print(str(searchsongQQ)+"已中止")
                                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,指令已被终止qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                        messagescucess = 1
                                                        messageRefresh = 0
                                                        break
                                                    else:
                                                        continue
                                            else:
                                                print('404')
                                        except:
                                            print('500')
                            elif songjson.get("code") == 404:
                                print(songjson.get("error"))
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,找不到对应的歌曲QAQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            else:
                                print(songjson.get("error"))
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(songjson.get("error"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            songmenumessage = "[CQ:face,id=9]呜呜，你没有指定对应的音乐平台QWQ。目前我支持以下音乐平台："
                            for songmenulist in songlist:
                                songmenumessage = songmenumessage+songmenulist+","
                            songmenumessage = songmenumessage+str('\n')+'(本功能接口来源于音乐搜索器，本机器人不存储任何的音乐)'+str('\n')+'-------------------'+str('\n')+MintBotVersion 
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(songmenumessage)})
                    elif '在吗' in messagecommand:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:poke,qq={}]'.format(qq)})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:face,id=147]'})
                    elif messagecommand[0:4] == '发送消息':
                        sendmessageidlist = []
                        if str(qq) in adminQQ:
                            if '到' in messagecommand:
                                if '群' in messagecommand:
                                    try:
                                        send_msg({'msg_type':'group','number':int(messagecommand[messagecommand.rfind('到')+1:messagecommand.rfind('群')]),'msg':str(messagecommand[4:messagecommand.rfind('到')])})
                                    except BaseException as error:
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                        print('所有异常的基类：'+str(error))
                                        continue
                                elif '人' in messagecommand:
                                    try:
                                        send_msg({'msg_type':'private','number':int(messagecommand[messagecommand.rfind('到')+1:messagecommand.rfind('人')]),'msg':str(messagecommand[4:messagecommand.rfind('到')])})
                                    except BaseException as error:
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                        print('所有异常的基类：'+str(error))
                                        continue
                                else:
                                    try:
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(messagecommand[4:len(messagecommand)])})
                                    except BaseException as error:
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                        print('所有异常的基类：'+str(error))
                                        continue
                            else:
                                try:
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(messagecommand[4:len(messagecommand)])})
                                except BaseException as error:
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                    print('所有异常的基类：'+str(error))
                                    continue
                        else:
                            try:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]您不是管理员QwQ"}) 
                            except BaseException as error:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                print('所有异常的基类：'+str(error))
                                continue
                    elif messagecommand[0:1] == '丢' or messagecommand[0:1] == '丟':
                        if messagecommand[1:2] == '我':
                            MoId = qq
                        elif 'CQ:at' in messagecommand:
                            MoId = messagecommand[messagecommand.rfind('=')+1:messagecommand.rfind(']')]
                        else:
                            MoId = messagecommand[1 :len(messagecommand)]
                        print(MoId)
                        DiuApiUrl = 'http://api.weijieyue.cn/api/tupian/diu.php?qq='+str(MoId)
                        os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                        Diufile = requests.get(DiuApiUrl)
                        Diufiletype = filetype.guess(Diufile.content).extension
                        with open(os.getcwd()+"\Diuimage."+Diufiletype,'wb') as f:
                            f.write(Diufile.content)
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\Diuimage."+Diufiletype+"]"})
                    elif messagecommand[0:1] == '赞':
                        if messagecommand[1:2] == '我':
                            MoId = qq
                        elif 'CQ:at' in messagecommand:
                            MoId = messagecommand[messagecommand.rfind('=')+1:messagecommand.rfind(']')]
                        else:
                            MoId = messagecommand[1:len(messagecommand)]
                        print(MoId)
                        ZanApiUrl = 'http://api.weijieyue.cn/api/tupian/zan.php?qq='+str(MoId)
                        os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                        Zanfile = requests.get(ZanApiUrl)
                        Zanfiletype = filetype.guess(Zanfile.content).extension
                        with open(os.getcwd()+"\Zanimage."+Zanfiletype,'wb') as f:
                            f.write(Zanfile.content)
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\Zanimage."+Zanfiletype+"]"})
                    elif messagecommand[0:1] == '爬':
                        if messagecommand[1:2] == '我':
                            MoId = qq
                        elif 'CQ:at' in messagecommand:
                            MoId = messagecommand[messagecommand.rfind('=')+1:messagecommand.rfind(']')]
                        else:
                            MoId = messagecommand[1:len(messagecommand)]
                        print(MoId)
                        PaApiUrl = 'http://api.weijieyue.cn/api/tupian/pa.php?qq='+str(MoId)
                        os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                        Pafile = requests.get(PaApiUrl)
                        Pafiletype = filetype.guess(Pafile.content).extension
                        with open(os.getcwd()+"\Paimage."+Pafiletype,'wb') as f:
                            f.write(Pafile.content)
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\Paimage."+Pafiletype+"]"})
                    elif messagecommand[0:2] == '摸摸':
                        if messagecommand[2:3] == '我':
                            MoId = qq
                        elif 'CQ:at' in messagecommand:
                            MoId = messagecommand[messagecommand.rfind('=')+1:messagecommand.rfind(']')]
                        else:
                            MoId = messagecommand[2:len(messagecommand)]
                        print(MoId)
                        MoApiQQimageUrl = 'http://api.btstu.cn/qqxt/api.php?qq='+str(MoId)
                        os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                        MoQQimagegetJson = demjson.decode(requests.get(MoApiQQimageUrl).text)
                        print(MoQQimagegetJson)
                        #MoApiul = 'http://api.wer.plus:8080/api/ruad?url=' + str(urllib.parse.quote(MoQQimagegetJson.get('imgurl'))) + '&token=' + str(onemingKey)
                        MoApiul = 'http://101.35.149.229:8080/api/ruad?url=' + str(urllib.parse.quote(MoQQimagegetJson.get('imgurl'))) + '&token=' + str(onemingKey)
                        print(MoApiul)
                        Mofilejsonget = requests.get(MoApiul).text
                        print(Mofilejsonget)
                        Mofilejson = demjson.decode(Mofilejsonget)
                        print(Mofilejson)
                        Mofile = requests.get(Mofilejson.get("url"))
                        Mofiletype = filetype.guess(Mofile.content).extension
                        with open(os.getcwd()+"\Moimage."+Mofiletype,'wb') as f:
                            f.write(Mofile.content)
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\Moimage."+Mofiletype+"]"})
                    elif messagecommand[0:4] == '摸鱼日历':
                        MoYuUrl = 'https://api.vvhan.com/api/moyu?type=json'
                        MoYuJsonGet = requests.get(MoYuUrl).text
                        MoYuJson = demjson.decode(MoYuJsonGet)
                        MoYuFile = requests.get(MoYuJson.get("url"))
                        MoYuFileType = filetype.guess(MoYuFile.content).extension
                        with open(os.getcwd()+"\MoYuimage."+MoYuFileType,'wb') as f:
                            f.write(MoYuFile.content)
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]摸鱼时间~~"+str("\n")+"[CQ:image,file=file:///"+os.getcwd()+"\MoYuimage."+MoYuFileType+"]"})
                    #elif messagecommand[0:2] == '测试':
                        #fururldata = {'qq':'2659170494','sign':furbotbuildSignString('api/v2/getFursuitRand',int(time.time()),'a4WpGePYVzMc6gSa'),'timestamp':int(time.time())}
                        #print(fururldata)
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(fururldata)})
                        #furget = requests.get("https://api.tail.icu/api/v2/getFursuitRand",data=fururldata).text
                        #print(furget)
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(furget)})
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜，咱不知道您说的指令QWQ。不妨说'薄荷本兽，菜单'看看我能做什么呗？"+str('\n')+"-------------------"+str('\n')+MintBotVersion})    
                #if message == "涂鸦宇宙":
                    #if 14<int(time.strftime("%H"))<16:
                        #continue
                    #else:
                        #continue
                if message == str(BotName):
                    print('收到菜单指令')
                    menumessage = '[CQ:face,id=12]嗷呜，欢迎使用'+BotName+'机器人，这是我可以做的事情OwO：'
                    for menulistline in menulist:
                        menumessage = menumessage + str("\n")+'[CQ:face,id=161]'+menulistline
                    menumessage = menumessage + str("\n")+"-------------------"+str("\n")+MintBotVersion
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':menumessage})
                if message == str("[CQ:at,qq="+QQID+"] ") or message == str("[CQ:at,qq="+QQID+"]"):
                    print('收到菜单指令')
                    menumessage = '[CQ:face,id=12]嗷呜，欢迎使用'+BotName+'机器人，这是我可以做的事情OwO：'
                    for menulistline in menulist:
                        menumessage = menumessage + str("\n")+'[CQ:face,id=161]'+menulistline
                    menumessage = menumessage + str("\n")+"-------------------"+str("\n")+MintBotVersion
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':menumessage})
                    
        except BaseException as error:
                   print('所有异常的基类：'+str(error))
                   continue
        except SystemExit as error:
                   print('解释器请求退出：'+str(error))
                   continue
        except KeyboardInterrupt as error:
                   print('用户中断执行(通常是输入^C)：'+str(error))
                   continue
#        except Exception as error:
#                   print('常规错误的基类：'+str(error))
#                   continue
        except StopIteration as error:
                   print('迭代器没有更多的值：'+str(error))
                   continue
        except GeneratorExit as error:
                   print('生成器(generator)发生异常来通知退出：'+str(error))
                   continue
        #except StandardError as error:
                   #print('所有的内建标准异常的基类：'+str(error))
                   #continue
        except ArithmeticError as error:
                   print('所有数值计算错误的基类：'+str(error))
                   continue
        except FloatingPointError as error:
                   print('浮点计算错误：'+str(error))
                   continue
        except OverflowError as error:
                   print('数值运算超出最大限制：'+str(error))
                   continue
        except ZeroDivisionError as error:
                   print('除(或取模)零 (所有数据类型)：'+str(error))
                   continue
        except AssertionError as error:
                   print('断言语句失败：'+str(error))
                   continue
        except AttributeError as error:
                   print('对象没有这个属性：'+str(error))
                   continue
        except EOFError as error:
                   print('没有内建输入,到达EOF 标记：'+str(error))
                   continue
        except EnvironmentError as error:
                   print('操作系统错误的基类：'+str(error))
                   continue
        except IOError as error:
                   print('输入/输出操作失败：'+str(error))
                   continue
        except OSError as error:
                   print('操作系统错误：'+str(error))
                   continue
        except WindowsError as error:
                   print('系统调用失败：'+str(error))
                   continue
        except ImportError as error:
                   print('导入模块/对象失败：'+str(error))
                   continue
        except LookupError as error:
                   print('无效数据查询的基类：'+str(error))
                   continue
        except IndexError as error:
                   print('序列中没有此索引(index)：'+str(error))
                   continue
        except KeyError as error:
                   print('映射中没有这个键：'+str(error))
                   continue
        except MemoryError as error:
                   print('内存溢出错误(对于Python 解释器不是致命的)：'+str(error))
                   continue
        except NameError as error:
                   print('未声明/初始化对象 (没有属性)：'+str(error))
                   continue
        except UnboundLocalError as error:
                   print('访问未初始化的本地变量：'+str(error))
                   continue
        except ReferenceError as error:
                   print('弱引用(Weak reference)试图访问已经垃圾回收了的对象：'+str(error))
                   continue
        except RuntimeError as error:
                   print('一般的运行时错误：'+str(error))
                   continue
        except NotImplementedError as error:
                   print('尚未实现的方法：'+str(error))
                   continue
        except SyntaxError as error:
                   print('Python 语法错误：'+str(error))
                   continue
        except IndentationError as error:
                   print('缩进错误：'+str(error))
                   continue
        except TabError as error:
                   print('Tab 和空格混用：'+str(error))
                   continue
        except SystemError as error:
                   print('一般的解释器系统错误：'+str(error))
                   continue
#        except TypeError as error:
#                   print('对类型无效的操作：'+str(error))
#                   continue
#        except ValueError as error:
#                   print('传入无效的参数：'+str(error))
#                   continue
        except UnicodeError as error:
                   print('Unicode 相关的错误：'+str(error))
                   continue
        except UnicodeDecodeError as error:
                   print('Unicode 解码时的错误：'+str(error))
                   continue
        except UnicodeEncodeError as error:
                   print('Unicode 编码时错误：'+str(error))
                   continue
        except UnicodeTranslateError as error:
                   print('Unicode 转换时错误：'+str(error))
                   continue
        except Warning as error:
                   print('警告的基类：'+str(error))
                   continue
        except DeprecationWarning as error:
                   print('关于被弃用的特征的警告：'+str(error))
                   continue
        except FutureWarning as error:
                   print('关于构造将来语义会有改变的警告：'+str(error))
                   continue
        #except OverflowWarning as error:
                   #print('旧的关于自动提升为长整型(long)的警告：'+str(error))
                   #continue
        except PendingDeprecationWarning as error:
                   print('关于特性将会被废弃的警告：'+str(error))
                   continue
        except RuntimeWarning as error:
                   print('可疑的运行时行为(runtime behavior)的警告：'+str(error))
                   continue
        except SyntaxWarning as error:
                   print('可疑的语法的警告：'+str(error))
                   continue
        except UserWarning as error:
                   print('用户代码生成的警告：'+str(error))
                   continue
#        except:
#                   print('未知错误')
#                   continue
        else:
            continue
    elif rev["post_type"]=="meta_event":
        print('消息为心跳类')
        continue
    elif rev["post_type"]=='notice':
        print('消息为通知类')
        try:
            if rev["sub_type"] == 'poke':
                if "group_id" in rev: 
                    sendid = rev['group_id']
                    qq=rev["sender_id"]
                    messagetype = 'group'
                else:            
                    sendid = rev["sender_id"]
                    qq = rev["sender_id"]
                    messagetype = 'private'
                if str(rev['target_id']) == str(QQID):
                    qq = rev['sender_id']
                    print('收到戳一戳机器人消息')
                    pokerandom = int(random.uniform(0, 50))
                    pokelistrandom = int(random.uniform(0, len(pokelist)))
                    if pokerandom < 25:
                        print('随机数小于25')
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:poke,qq='+str(qq)+']'})
                    elif pokerandom == 25:
                        print('随机数等于25')
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:poke,qq='+str(qq)+']'})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+str(qq)+']'+str(pokelist[pokelistrandom])})
                    elif pokerandom > 25:
                        print('随机数大于25')
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+str(qq)+']'+str(pokelist[pokelistrandom])})
                    else:
                        #print('随机数获取出错')
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+str(qq)+']随机数获取失败了呜呜QAQ'})
                        print('随机数转整数出错(可能等于小于0)，默认识别为小于25')
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:poke,qq='+str(qq)+']'})
            else:
                continue
        except KeyError as error:
            print('Json找不到值：'+str(error))
            continue        
    else:
        continue
