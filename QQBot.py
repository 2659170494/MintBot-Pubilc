# -*- coding: UTF-8 -*-import receive
import base64
import WebFurApi
import WebMediaApi
import BCMCreator
import SMM2API
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
import threading
from ast import Continue
from cmath import exp
from keyword import kwlist
savelist=['DebugGroupID','QQID','DebugQQID','adminQQ','superadmin','weatherKEY','onemingKey','BcmcreatorOA','furauthKey','furauthqq','ZlibUserEmail','ZlibPassword','privateblacklist','groupblacklist','bcxVIPid','bcxjson','bcxVIPCode',"ChatLastTime","ChatLastID",'ChatMessageAllow','ChatUserIDJson']  #需要存读的变量
def crashlogsave(text):
    if os.path.exists(os.getcwd()+r'/botcrashlog.txt')==True:
        print('日志文件存在，开始保存错误')
        crashlogfile = open(os.getcwd()+r'/botcrashlog.txt', mode='r+')
    elif os.path.exists(os.getcwd()+r'/botcrashlog.txt')==False:
        print('日志文件不存在，开始自动创建')
        crashlogfile = open(os.getcwd()+r'/botcrashlog.txt', mode='w+')
    else:
        print('日志文件存取失败：出现异常错误')
        exit()
    if str(crashlogfile.read()) == '':
        crashlogfile.write(crashlogfile.read()+"("+str(time.asctime( time.localtime(time.time()) ))+")"+str(text)+"\n")
    else:
        crashlogfile.write(crashlogfile.read()+"("+str(time.asctime( time.localtime(time.time()) ))+")"+str(text)+"\n")
    crashlogfile.close()
    print("日志保存完毕")
def save_save():  #保存存档
    try:  #尝试执行代码
        savefile = open(os.getcwd()+r'/botsave.txt', mode='w+')   #打开文件
        #print(savefile)
        globallist = globals()  #读取全局变量
        #print(globallist)
        savedict ={}  #预设需要保存的变量字典
        #print(savedict)
        for val in savelist:  #从需要要保存的变量的列表中读取出变量名到val变量直到读取完毕
            #print(val)
            savetempdict={val:globallist[val]} #设置缓存列表为(变量名:变量的内容)
            #print(savetempdict)
            savedict.update(savetempdict) #添加缓存列表数据到变量字典
            #print(savedict)
        savefile.write(demjson.encode(savedict)) #将字典转换成json之后写入文件
        #print(json.dumps(savedict))
        savefile.close() #关闭文件
        print('存档完毕')
    except BaseException as error: #抓取try代码中所有错误的类型和原因给error并执行代码
        print('发生错误QAQ:'+str(error))
        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)}) #发送消息模块
        crashlogsave("保存存档:"+str(error)) #保存日志文件
def save_read():  #读取存档
    try:  #尝试执行代码
        savefile = open(os.getcwd()+r'/botsave.txt', mode='r+')  #读取文件
        savereaddata  =  demjson.decode(savefile.read()) #读取文件中的json并转换成字典
        #print(savereaddata)
        for val in savereaddata: #从字典中找出变量并赋值给val直至查找完毕
            #print(val)
            #print(evalcommand)
            #print('global '+val+';'+val+'='+str(savereaddata[val]))
            #print(str(type(savereaddata[val])))
            if str(type(savereaddata[val])) == "<class 'str'>": #判断要存档的变量是不是字符串类型，如果是就在代码中加引号。反之不加
                exec('global '+val+' ; '+val+"='"+str(savereaddata[val])+"'") #以全局模式调用代码(是字符串类型，而不是在函数里调用代码)
            else:
                exec('global '+val+' ; '+val+"="+str(savereaddata[val])) #以全局模式调用代码(非字符串类型，而不是在函数里调用代码)
            savefile.close()   #关闭文件
        #print( locals())
        print('读档完毕')
    except IOError: #捕获输入/出错误和原因给error并执行代码
        print('没有存档文件QWQ')
        crashlogsave("读取存档:没有存档文件QWQ") #保存日志文件
        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：没有存档文件'}) #发送消息模块
    except BaseException as error: #捕获所有错误和原因给error并执行代码
        print('发生错误QAQ:'+str(error))
        crashlogsave("读取存档:"+str(error)) #保存日志文件
        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)}) #发送消息模块
#下面是一些配置。
Debug = 0 #调试开关
DebugGroupID = 0 #调试专用群
DebugQQID = 0 #调试专用QQ号
QQID="" #机器人的QQ号
adminQQ = [''] #管理员QQ列表
superadmin = '' #超级管理员(机主)
TuYaApiID = "" #涂鸦找找API ID
TuYaApiKey = ""#涂鸦找找API Key
weatherKEY = '' #和风天气WebAPI的KEY
#onemingKey = '' #一铭API(https://api.wer.plus/)密钥
BcmcreatorOA = '' #编创协OA密钥
furauthKey = '' #绒狸开源机器人KEY,若没有请联系官方获取(密钥仅V2需使用，V1不受影响)
furauthqq = '' #绒狸开源机器人KEY关联的QQ号
ZlibUserEmail = '' #服务器出现问题(或者说被墙了)，暂时停止维护
ZlibPassword = '' #服务器出现问题(或者说被墙了)，暂时停止维护
cqhttpserverip = '127.0.0.1' #CQ-Http服务器地址(Go-Cqhttp)
cqhttpserveriphost = 5700 #CQ-Http服务器地址端口(Go-Cqhttp)
cqhttpposthost = 5701 #CQ-Http服务器反向Post端口
cqhttpaccesstoken = '' #连接CQ-Http服务器用的access_token，没有则留空
proxyserverip = "127.0.0.1" #HTTP代理服务器的IP地址
proxyserverhost = 33210 #HTTP代理服务器的端口号
MintBotVersion = 'MintBot V20230104' #机器人版本号
BotName = '薄荷本兽' #机器人名字
ZlibraryURL = 'zh.cn1lib.vip' #目前zlibrary有镜像网站，但是不清楚是否支持API调用，完整版本将会在v2版本开发
menulist = ['---通知类---',BotName+',赞助名单 ---返回从头以来的所有捐助记录','---搜图类---',BotName+',涂鸦找找(名字) ---在涂鸦宇宙中查找小伙伴并随机返回小伙伴的图片',BotName+',绒狸找找(名字) ---在绒狸API中查找兽兽并随机返回毛图',BotName+',绒狸来只毛 ---随机在绒狸API获取一张毛图片',BotName+',云绒来只毛 ---随机在兽云祭API获取一张毛图片',BotName+',云绒找找---在兽云祭API中查找兽兽并随机返回毛图',BotName+',丢(/赞/爬/摸摸)(QQ号) ---(维护中，API商跑路了XwX。后续打算手动移植)发送自定义表情','---日常类---',BotName+',今日早报 ---查看今日的60秒早报',BotName+',(城市)天气 ---在和风天气查找对应城市的实时天气',BotName+',(音乐平台)搜歌(歌名) ---在音乐搜索器API搜索歌曲(若不知道支持平台可以把平台名字留空后发送查看)',BotName+',摸鱼日历 ---[维护中(不稳)，等待多线程功能中）]调用韩小韩API获取今日摸鱼日历','---安全类---',BotName+',沙盒分析 ---[开发中]调用微步在线API进行文件分析','---娱乐类---',BotName+',网络天才 ---[开发和爬虫中]让你不用下载软件和梯子就可以玩?(但是真做的话麻烦qwq)',BotName+',马造找找(ID) ---通过外网API查找马里奥制造2的关卡或者作者的信息','---注意事项---','1.功能备注加方框的为暂时无法使用的功能，通常都在维护或者开发中(也有可能遇到了bug)','2.本机器人大部分功能都取自于互联网的API，信息不一定准确。仅供参考','3.禁止使用机器人进行刷屏、骚扰等进行一些违法违纪的事情，本机器人有权限制您的功能但不限于拉入黑名单','4.本机器人拥有一些专属功能，一般不外透','5.本机器人因开发需要，拥有公开的控制机器人发言API。如果有因为机器人被控制而发言出异常的行为，均可对机器人做出禁言或踢出的行为'] #机器人目前支持的功能
pokelist = [' 嗷呜OwO',' 呜呜不要再戳了QwQ',' 哇啊好痛QAQ',' awa',' 喵呜OwO',' ~~'," 好痛QAQ"] #机器人被戳一戳后会随机发送的消息
songlist = ['网易云','QQ音乐','(维护中)酷狗','酷我','千千','一听','咪咕','荔枝','蜻蜓','喜马拉雅','5sing原创','5sing翻唱','全民K歌'] #目前音乐搜索器支持的音乐平台
zanzhutime = "2022年09月04日"
zanzhurenlist = ["辉煌余光 -- 20元(2022年09月04日)","冷鱼与热猫 -- 10元(2022年07月08日)","和泉纱雾 -- 5元(2022年11月10日)","星舰earth -- 1元(2022年10月19日)","过客 -- 1元(2022年10月19日)","柒夏鸭 -- 1元(2022年10月21日)","Indev_Classic -- 1元(2022年10月13日)","绿色耀西 -- 技术与服务器维护(191.93元(不完全统计QwQ,2022年01月18日~至今))"]
bcxmenulist = ['......绑定菜单......','#登录 [code] (仅限官群)','#退出登录 (仅限官群)','......数据查询......','#同步编程猫昵称','#个人数据','#查询数据 [@SomeBody]','#日志 [@SomeBody或编程猫ID]','#委员日志 [@SomeBody或编程猫ID]','#全局日志(仅限管理)','#本周排名(仅限管理)','#查询Null精神状态',"#开启聊天室收发信","#关闭聊天室收发信","#展示最新文章",'......温馨提示......','1.绑定Code获取：'+r'https://bcmcreator.cn/index.php?mod=OAuth','2.全局日志和本周排名只有管理和群主才能使用，因为有刷屏的风险','3.账号一旦绑定了机器人后，本机器人有权保存由编创协API返回您的账号的资料以便后续进行您需要的操作，想要删除资料只需退出登陆即可。但是！！在退群后仍然会保存在数据库中，如有异议可以联系耀西或冷鱼进行协调','4.除特殊声明外，您可以把机器人拉进您拥有管理或者群主权限的群(记得跟耀西说一声，不说也行awa)以使用管理员专属功能(但是禁止对机器人进行占用或刷屏)','5.一般情况下，使用本机器人功能如果遇到刷屏等其他异常现象，只要非故意行为且没有触犯群规均可饶恕','6.因为本机器人有对外公开的发送消息API，所以。。。如果咱说了什么奇怪的话。。。尽量原谅咱QwQ','7.#号请用半角(英文符号)的，不要用全角(中文符号)XwX','8.<本菜单下所有功能的最终解释权由编创协所属>']
privateblacklist = [] #私聊黑名单
groupblacklist = [] #群聊黑名单
bcxjson = {}
bcxVIPid = {}
bcxVIPCode = []
ChatLastTime = ""
ChatLastID = ""
ChatLastIDList = []
ChatMessageAllow = 1
ChatUserIDJson = {}
#上面是一些配置
if os.path.exists(os.getcwd()+r'/botsave.txt')==True:
    print('检测到存档文件，开始读档')
    save_read()
elif os.path.exists(os.getcwd()+r'/botsave.txt')==False:
    print('存档不存在，开始自动创建')
    save_save()
else:
    print('读取失败：出现错误')
    crashlogsave("读取存档失败:出现错误？("+os.path.exists(os.getcwd()+r'/botsave.txt')+")")
    exit()
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
str(QQID)
print('机器人QQ号:'+str(QQID))
print('超级管理员QQ：'+str(superadmin))
print('和风天气API的KEY：'+weatherKEY)
#print('一铭API密钥：'+str(onemingKey))
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
print('编创协会员列表：'+str(bcxVIPid))
print('编创协已使用的会员证：'+str(bcxVIPCode))
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
    msg = urllib.parse.quote(msg)
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
        msg = msg.replace("[","&#91;")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("]","&#93;")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("[","%26#91;")
    except BaseException as error:
        #print('所有异常的基类：'+str(error))
        Continue
    try:
        msg = msg.replace("]","%26#93;")
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
    try:
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
            thesearchmusiccode=str(songjson.get("code"))
            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(songjson.get("error"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
            crashlogsave("音乐搜索:(这是调用API时发生的错误)"+f"({thesearchmusiccode})"+str(songjson.get("error")))
            return songjson.get("code")
    except BaseException as error:
        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,出错了QAQ：API可能出现了异常"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
        crashlogsave("音乐搜索:(这是在用户执行下一页或上一页时发生的错误)"+str(error))
    
class mythread(threading.Thread):
    def __init__(self,defun,threadID,name,delay):
        threading.Thread.__init__(self)
        self.threadID = 1
        self.name = "waittime"
        self.delay = 1
    def run(self,defun):
        print ("开始线程：" + self.name)
        defun()
        print ("退出线程：" + self.name)
try:
    #ChatLastTimerequests = BCMCreator.GetChat_local(11,15)
    ChatLastTimerequests = BCMCreator.GetChat(11,15)
    print(ChatLastTimerequests)
    ChatLastTimeJson = demjson.decode(ChatLastTimerequests)
    for line1 in range(1,len(ChatLastTimeJson)+1):
        line = ChatLastTimeJson[int(line1)*-1]
        ChatLastTime = str(line.get("time"))
        ChatLastID = str(line.get("id"))
        ChatLastIDList.append(str(line.get("id")))
        #print(ChatLastID)
        #print(ChatLastTime)
    print("BCMcreator:初始化完毕")
except BaseException as error:
    ChatMessageAllow =0
    crashlogsave("BCMcreator(聊天室收发):"+str(error))
    print("BCMcreator:初始化失败，已关闭聊天室收发消息功能")

def chatfind():
    messagetype = "group"
    sendid = "982923687"
    #sendid = "1009481093"
    #print("BCMcreator:开始检查消息")
    while True:
        if str(ChatMessageAllow) == "1":
            #print("BCMcreator:时间已到，开始检查消息")
            time.sleep(10)
            #chatjson = json.loads(BCMCreator.GetChat_local(19,1))
            #chatjson = demjson.decode(BCMCreator.GetChat_local(11,15))
            chatjson = demjson.decode(BCMCreator.GetChat(11,15))
            chattmpmessage = ""
            #print(chatjson)
            for line1 in range(1,len(chatjson)+1):
                line = chatjson[int(line1)*-1]
                #print(line)
                #if str(line.get("time"))[len(str(line.get("time")))-8:len(str(line.get("time")))] >= ChatLastTime[len(ChatLastTime)-8:len(ChatLastTime)]:
                if str(line.get("time")) >= ChatLastTime:
                    if str(line.get("sender_id")) != "19":
                        #print(str(line.get("id")))
                        if str(line.get("id")) != str(ChatLastID):
                            if str(str(line.get("id")) in ChatLastIDList) == "False":
                                print("BCMcreator:获得到最新消息:"+line.get("message"))
                                try:
                                    #for user in demjson.decode(BCMCreator.getChatUser_user_name_local(line.get("sender_id"))):
                                    for user in demjson.decode(BCMCreator.getChatUser_user_name(line.get("sender_id"))):
                                        sendname = user.get("first_name")
                                except:
                                    sendname = "未知用户(无法通过ID正确查找到该用户)"
                                chatuserid = str(line.get("sender_id"))
                                if chattmpmessage != "":
                                    chattmpmessage = chattmpmessage + "\n" + f'网络聊天室[{sendname}(ID:{chatuserid})]:'+line.get("message")
                                else:
                                    chattmpmessage = chattmpmessage + f'网络聊天室[{sendname}(ID:{chatuserid})]:'+line.get("message")
                                lasttime = line.get("time")
                                lastid = str(line.get("id"))
                                exec(f"global ChatLastTime;ChatLastTime = '{lasttime}'")
                                exec(f"global ChatLastID;ChatLastID = '{lastid}'")
                                exec(f"global ChatLastIDList;ChatLastIDList.append({lastid})")
                                save_save()
            if chattmpmessage != "":
                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':chattmpmessage})
            #print("BCMcreator:检查完毕，开始等待3秒")

def getfile2tempfilelink(QQID):
    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':f"[CQ:at,qq={QQID}] 请发送文件到群文件中"})

def MoYuDayDef(messagetype,sendid,qq):
    MoYuUrl = 'https://api.vvhan.com/api/moyu?type=json'
    MoYuJsonGet = requests.get(MoYuUrl).text
    MoYuJson = demjson.decode(MoYuJsonGet)
    MoYuFile = requests.get(MoYuJson.get("url"))
    MoYuFileType = filetype.guess(MoYuFile.content).extension
    with open(os.getcwd()+"\MoYuimage."+MoYuFileType,'wb') as f:
        f.write(MoYuFile.content)
    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':f"[CQ:at,qq={qq}][CQ:face,id=12]摸鱼时间~~"+str("\n")+"[CQ:image,file=file:///"+os.getcwd()+"\MoYuimage."+MoYuFileType+"]"})

for i in range(1):
    t = threading.Thread(target=chatfind)
    t.start()

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
                    if str(sendid) == "982923687" and str(ChatMessageAllow) == "1":
                        #BCMCreator.RoomChat_local("19","11",f"编程极星创作者协会会员群:{message}")
                        #if str(qq) in ChatUserIDJson:
                            #try:
                                #final = json.loads(BCMCreator.RoomChat_local(ChatUserIDJson[str(qq)],"11",f"{message}"))
                                #final = json.loads(BCMCreator.RoomChat_meid_local(ChatUserIDJson[str(qq)],"11",f"{message}"))
                                #print(final)
                                #if str(final.get("code")) != "200":
                                    #peoplename = rev["sender"]["nickname"]
                                    #final = BCMCreator.RoomChat_local("19","11",f"{peoplename}：{message}")
                                    #print(final)
                            #except:
                                #peoplename = rev["sender"]["nickname"]
                                #final = BCMCreator.RoomChat_local("19","11",f"{peoplename}：{message}")
                                #print(final)
                        #else:
                        if message[0:1] == "#" or message[0:len(BotName)] == str(BotName) or message[0:len(message)] == "[CQ:at,qq="+QQID+"]" or message[0:len(message)] == "[CQ:at,qq="+QQID+"] ":
                            pass
                        else:
                            if str(qq) in bcxVIPid:
                                print("BCMcreator:该会员已和机器人绑定")
                                try:
                                    #final = json.loads(BCMCreator.RoomChat_meid_local(bcxVIPid.get(str(qq)),"11",message,"654059"))
                                    final = json.loads(BCMCreator.RoomChat_meid(bcxVIPid.get(str(qq)),"11",message,"654059"))
                                    #print(final)
                                    if str(final.get("code")) != "200":
                                        print("BCMcreator:使用该会员ID时无法发送消息，已自动转用19:"+str(final))
                                        peoplename = rev["sender"]["nickname"]
                                        #final = BCMCreator.RoomChat_local("19","11",f"{peoplename}：{message}")
                                        #final = json.loads(BCMCreator.RoomChat_meid_local("19","11",f"{peoplename}：{message}","654059"))
                                        final = json.loads(BCMCreator.RoomChat_meid("19","11",f"{peoplename}：{message}","654059"))
                                        print(final)
                                    else:
                                        Bcxlastid = final.get("uid")
                                        ChatLastIDList.append(Bcxlastid)
                                        #ChatLastID = Bcxlastid
                                        #exec(f"global ChatLastID;ChatLastID = '{Bcxlastid}'")
                                        #exec(f"global ChatLastIDList;ChatLastIDList.append({Bcxlastid})")
                                        print("BCMcreator:使用会员ID发送消息成功，消息ID为:"+str(Bcxlastid))
                                        save_save()
                                except:
                                    print("BCMcreator:编创协会员ID获取失败")
                                    peoplename = rev["sender"]["nickname"]
                                    #final = BCMCreator.RoomChat_local("19","11",f"{peoplename}：{message}")
                                    #final = json.loads(BCMCreator.RoomChat_meid_local("19","11",f"{peoplename}：{message}","654059"))
                                    final = json.loads(BCMCreator.RoomChat_meid("19","11",f"{peoplename}：{message}","654059"))
                            else:
                                peoplename = rev["sender"]["nickname"]
                                #final = BCMCreator.RoomChat_local("19","11",f"{peoplename}：{message}")
                                #final = json.loads(BCMCreator.RoomChat_meid_local("19","11",f"{peoplename}：{message}","654059"))
                                final = json.loads(BCMCreator.RoomChat_meid("19","11",f"{peoplename}：{message}","654059"))
                                #print(final)
                if rev["message_type"] == "private":
                    sendid = rev['sender']['user_id']
                    message = rev["raw_message"]
                    qq = rev['sender']['user_id']
                    messagetype = 'private'
                    try:
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'收到来自'+str(sendid)+'的消息：'+str(message)})
                        Continue
                    except BaseException as error:
                        crashlogsave("私聊转发管理:"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'收到消息但发送了错误QAQ：'+str(error)})
                        Continue
                    wmsucessful =1
                #print('消息为群消息类')
                print('消息为群聊和私聊消息类')
                if "[CQ:at,qq="+QQID+"]" in message:
                    if rev['raw_message'][len(rev['raw_message'])-2:len(rev['raw_message'])]=='在吗':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:poke,qq={}]'.format(qq)})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:face,id=147]'})
                elif message[0:4] == '#登录 ' or message[0:4] == '#登陆 ' or message[0:4] == '#登入 ' or message[0:4] == '#绑定 ':
                    logininbcxgroup = 0
                    if messagetype == 'group':
                        if str(sendid) == "599683567" or str(sendid) == "982923687" or str(sendid) == "1009481093":
                            logininbcxgroup = 1
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]呜呜，目前这个功能只能在官方协会群使用。如有疑问可以直接私聊留言'})
                            continue
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]呜呜，目前这个功能只能在官方协会的群使用。如有疑问可以直接私聊留言'})
                        continue
                    try:
                        bcxcode = message[4:len(message)]
                        print(bcxcode)
                        if bcxcode.isdigit() == False:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]呜呜，您输入的code格式不正确XwX'})
                            continue
                        #bcxcodejson=demjson.decode(BCMCreator.user_info_code_Plus_local(bcxcode))
                        bcxcodejson=demjson.decode(BCMCreator.user_info_code_Plus(bcxcode))
                        if str(bcxcodejson.get("code")) == '200':
                            bcxjson[str(qq)]=demjson.encode(bcxcodejson)
                            bcxVIPid[str(qq)] = bcxcodejson.get("uid")
                            save_save()
                            #print(str(BCMCreator.user_destroyCode_local(bcxcode)))
                            print(str(BCMCreator.user_destroyCode(bcxcode)))
                            #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]绑定成功\n[CQ:image,file='+bcxcodejson.get("picture")+']\n训练名字：'+str(bcxcodejson.get("name"))+'\n训练家ID：'+str(bcxcodejson.get("uid"))+'\n您可是'+str(bcxcodejson.get('Membershipgrade'))+'，拥有'+str(bcxcodejson.get('integral'))+'积分哇!awa\n还有，欢迎来到编创协!'})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]账号与本机器人绑定成功\n[CQ:image,file='+bcxcodejson.get("picture")+']\n会员昵称：'+str(bcxcodejson.get("name"))})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]绑定失败('+str(bcxcodejson.get('code'))+'):'+str(bcxcodejson.get('msg'))+'\n友情提示:code不是编程猫ID，如果您不知道code或者没有code，请去'+r'https://bcmcreator.cn/index.php?mod=OAuth'+'申请code'})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#登录):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]绑定失败(连接服务器失败):'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                elif message[0:3] == '#登录' or message[0:3] == '#登陆' or message[0:3] == '#登入' or message[0:3] == '#绑定':
                    logininbcxgroup = 0
                    if messagetype == 'group':
                        if str(sendid) == "599683567" or str(sendid) == "982923687" or str(sendid) == "1009481093":
                            logininbcxgroup = 1
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]呜呜，目前这个功能只能在官方协会群使用。如有疑问可以直接私聊留言'})
                            continue
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]呜呜，目前这个功能只能在官方协会的群使用。如有疑问可以直接私聊留言'})
                        continue
                    try:
                        bcxcode = message[3:len(message)]
                        print(bcxcode)
                        if bcxcode.isdigit() == False:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]呜呜，您输入的code格式不正确XwX'})
                            continue
                        #bcxcodejson=demjson.decode(BCMCreator.user_info_code_Plus_local(bcxcode))
                        bcxcodejson=demjson.decode(BCMCreator.user_info_code_Plus(bcxcode))
                        if str(bcxcodejson.get("code")) == '200':
                            bcxjson[str(qq)]=demjson.encode(bcxcodejson)
                            bcxVIPid[str(qq)] = bcxcodejson.get("uid")
                            save_save()
                            #print(str(BCMCreator.user_destroyCode_local(bcxcode)))
                            print(str(BCMCreator.user_destroyCode(bcxcode)))
                            #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]绑定成功\n[CQ:image,file='+bcxcodejson.get("picture")+']\n训练名字：'+str(bcxcodejson.get("name"))+'\n训练家ID：'+str(bcxcodejson.get("uid"))+'\n您可是'+str(bcxcodejson.get('Membershipgrade'))+'，拥有'+str(bcxcodejson.get('integral'))+'积分哇!awa\n还有，欢迎来到编创协!'})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]账号与本机器人绑定成功\n[CQ:image,file='+bcxcodejson.get("picture")+']\n会员昵称：'+str(bcxcodejson.get("name"))})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]绑定失败('+str(bcxcodejson.get('code'))+'):'+str(bcxcodejson.get('msg'))+'\n友情提示:code不是编程猫ID，如果您不知道code或者没有code，请去'+r'https://bcmcreator.cn/index.php?mod=OAuth'+'申请code'})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#登录):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]绑定失败(连接服务器失败):'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                #elif message[0:6] == "#群聊绑定 " or message[0:7] == "#聊天室绑定 ":
                    #if message[0:6] == "#群聊绑定 ":
                        #ChatUserIDJson[str(qq)] = message[6:len(message)]
                    #else:
                        #ChatUserIDJson[str(qq)] = message[7:len(message)]
                    #save_save()
                    #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]群聊绑定成功,您绑定的用户ID为:'+ChatUserIDJson[str(qq)]})
                #elif message[0:5] == "#群聊绑定" or message[0:6] == "#聊天室绑定":
                    #if message[0:5] == "#群聊绑定":
                        #ChatUserIDJson[str(qq)] = message[5:len(message)]
                    #else:
                        #ChatUserIDJson[str(qq)] = message[6:len(message)]
                    #save_save()
                    #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]群聊绑定成功,您绑定的用户ID为:'+ChatUserIDJson[str(qq)]})
                #elif message[0:8] == '#取消群聊绑定 ' or message[0:9] == '#取消聊天室绑定 ' or message[0:8] == '#退出群聊绑定 ' or message[0:9] == '#退出聊天室绑定 ' or message[0:8] == '#登出群聊绑定 ' or message[0:9] == '#登出聊天室绑定 ':
                    #del ChatUserIDJson[str(qq)]
                    #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]退出绑定成功'})
                #elif message[0:7] == '#取消群聊绑定' or message[0:8] == '#取消聊天室绑定' or message[0:7] == '#退出群聊绑定' or message[0:8] == '#退出聊天室绑定' or message[0:7] == '#登出群聊绑定' or message[0:8] == '#登出聊天室绑定':
                    #del ChatUserIDJson[str(qq)]
                    #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]退出绑定成功'})
                elif message[0:5] == '#退出登录' or message[0:5] == '#退出登陆' or message[0:5] == '#退出登入':
                    logininbcxgroup = 0
                    if messagetype == 'group':
                        if str(sendid) == "599683567" or str(sendid) == "982923687" or str(sendid) == "1009481093":
                            logininbcxgroup = 1
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]呜呜，目前这个功能只能在官方协会群使用。如有疑问可以直接私聊留言'})
                            continue
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]呜呜，目前这个功能只能在官方协会的群使用。如有疑问可以直接私聊留言'})
                        continue
                    try:
                        del bcxjson[str(qq)]
                        del bcxVIPid[str(qq)]
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]退出登录(删除本地数据库数据)成功'})
                    except:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]删除失败:可能您的账号没有与机器人绑定，咱在自己的数据库找不到您的信息哇QwQ'})
                        #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        continue
                elif message[0:5] == '#个人数据' or message[0:5] == '#个人资料' or message[0:5] == '#个人信息':
                    try:
                        try:
                            bcmcode = bcxVIPid[str(qq)]
                        except:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:可能您的账号没有与机器人绑定，咱在自己的数据库找不到您的信息哇QwQ'})
                            #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                            continue
                        #bcxinfo = json.loads(BCMCreator.user_info_local(bcmcode), strict=False)
                        bcxinfo = json.loads(BCMCreator.user_info(bcmcode), strict=False)
                        if bcxinfo.get("code") == '200':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]您好哇!awa\n[CQ:image,file='+bcxinfo.get("picture")+']\n会员昵称:'+str(bcxinfo.get("name"))+'\n会员积分:'+str(bcxinfo.get("integral"))+'\n会员等级:'+str(bcxinfo.get("Membershipgrade"))+'\n会员头衔:'+str(bcxinfo.get('title'))+'\n会员的帅气签名[CQ:face,id=12]:'+str(bcxinfo.get('introduce'))})
                        elif bcxinfo.get("code") == '404':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:咱没有在服务器数据库找到您哇，要不问问鱼鱼QwQ?'})
                            #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                            send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#个人资料):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                elif message[0:6] == '#查询数据 ' or message[0:6] == '#查询资料 ' or message[0:6] == '#查询信息 ' or message[0:6] == '#查找数据 ' or message[0:6] == '#查找资料 ' or message[0:6] == '#查找信息 ':
                    try:
                        bcxguess = message[6:len(message)]
                        bcxqq = bcxguess[bcxguess.rfind('=')+1:bcxguess.rfind(']')]
                        print(bcxqq)
                        try:
                            bcmcode = bcxVIPid[str(bcxqq)]
                        except:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:可能您要查找的账号没有与机器人绑定(或许您提供的信息是编程猫ID或者是空?我们目前只接受从QQ的@获取到的QQ号)，咱在自己的数据库找不到您的信息哇QwQ'})
                            #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                            continue
                        #bcxinfo = demjson.decode(BCMCreator.user_info_local(bcmcode))
                        bcxinfo = demjson.decode(BCMCreator.user_info(bcmcode))
                        if bcxinfo.get("code") == '200':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]已经为您查询到我此会员了!awa\n[CQ:image,file='+bcxinfo.get("picture")+']\n会员昵称:'+str(bcxinfo.get("name"))+'\n会员积分:'+str(bcxinfo.get("integral"))+'\n会员等级:'+str(bcxinfo.get("Membershipgrade"))+'\n会员头衔:'+str(bcxinfo.get('title'))+'\n会员的帅气签名[CQ:face,id=12]:'+str(bcxinfo.get('introduce'))})
                        elif bcxinfo.get("code") == '404':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:咱没有在服务器数据库找到您要找的人哇，要不问问鱼鱼QwQ?'})
                            #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                            send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#查询资料):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                elif message[0:5] == '#查询数据' or message[0:5] == '#查询资料' or message[0:5] == '#查询信息' or message[0:5] == '#查找数据' or message[0:5] == '#查找资料' or message[0:5] == '#查找信息':
                    try:
                        bcxguess = message[5:len(message)]
                        bcxqq = bcxguess[bcxguess.rfind('=')+1:bcxguess.rfind(']')]
                        print(bcxqq)
                        try:
                            bcmcode = bcxVIPid[str(bcxqq)]
                        except:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:可能您要查找的账号没有与机器人绑定(或许您提供的信息是编程猫ID或者是空?我们目前只接受从QQ的@获取到的QQ号)，咱在自己的数据库找不到您的信息哇QwQ'})
                            #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                            continue
                        #bcxinfo = demjson.decode(BCMCreator.user_info_local(bcmcode))
                        bcxinfo = demjson.decode(BCMCreator.user_info(bcmcode))
                        if bcxinfo.get("code") == '200':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]已经为您查询到我此会员了!awa\n[CQ:image,file='+bcxinfo.get("picture")+']\n会员昵称:'+str(bcxinfo.get("name"))+'\n会员积分:'+str(bcxinfo.get("integral"))+'\n会员等级:'+str(bcxinfo.get("Membershipgrade"))+'\n会员头衔:'+str(bcxinfo.get('title'))+'\n会员的帅气签名[CQ:face,id=12]:'+str(bcxinfo.get('introduce'))})
                        elif bcxinfo.get("code") == '404':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:咱没有在服务器数据库找到您要找的人哇，要不问问鱼鱼QwQ?'})
                            #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                            send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#查询资料):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                #elif message[0:6] == '#查询执行人' and message[len(message)-3:bcxguess.rfind('志')+1] == '行日志' or message[0:6] == '#查找执行人' and message[len(message)-3:bcxguess.rfind('志')+1] == '行日志':
                elif message[0:4] == '#日志 ':
                    try:
                        # bcxguess = message[bcxguess.rfind('志')+1:len(message)]
                        #print(bcxguess)
                        #print(message[6:bcxguess.rfind('行')])
                        #loglimit = int(message[6:bcxguess.rfind('行')])
                        bcxguess = message[4:len(message)]
                        print(bcxguess)
                        if 'CQ:at' in bcxguess:
                            bcxqq = bcxguess[bcxguess.rfind('=')+1:bcxguess.rfind(']')]
                        else:
                            bcxqq = bcxguess
                        print(bcxqq)
                        if 'CQ:at' in bcxguess:
                            try:
                                bcmcode = bcxVIPid[str(bcxqq)]
                            except:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:可能您要查找的账号没有与机器人绑定(或许您提供的信息是编程猫ID或者是空?我们目前只接受从QQ的@获取到的QQ号)，咱在自己的数据库找不到您的信息哇QwQ'})
                                #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                                continue
                        else:
                            bcmcode = bcxqq
                        print(bcmcode)
                        #bcxloginfo = json.loads(BCMCreator.association_log_id_local(bcmcode,3), strict=False)
                        bcxloginfo = json.loads(BCMCreator.association_log_id(bcmcode,3), strict=False)
                        #if bcxinfo.get("code") == '200':
                        if 'code' in bcxloginfo:
                            if bcxloginfo.get("code") == '404':
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:咱没有在服务器数据库找到您要找的人的日志哇，要不问问鱼鱼QwQ?'})
                                #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        else:
                            #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                            #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                            bxclogmessage = "[CQ:at,qq="+str(qq)+"]\n成功查询到关于此人的日志awa:\n"
                            bxclogmessageline = 1
                            for line in bcxloginfo:
                                #line = demjson.decode(line)
                                bxclogmessage = bxclogmessage + '------第'+str(bxclogmessageline)+'条------\n时间:' + str(line.get('time')) + '\n委员:' + str(line.get("name")) + '\n原因:' + str(line.get('yy')) +'\n'
                                bxclogmessageline = bxclogmessageline + 1
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':bxclogmessage})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#日志):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                #elif message[0:6] == '#查询执行人' and message[len(message)-4:bcxguess.rfind('志')+2] == '行日志 ' or message[0:6] == '#查找执行人' and message[len(message)-4:bcxguess.rfind('志')+2] == '行日志 ':
                elif message[0:3] == '#日志':
                    try:
                        # bcxguess = message[bcxguess.rfind('志')+1:len(message)]
                        #print(bcxguess)
                        #print(message[6:bcxguess.rfind('行')])
                        #loglimit = int(message[6:bcxguess.rfind('行')])
                        bcxguess = message[3:len(message)]
                        print(bcxguess)
                        if 'CQ:at' in bcxguess:
                            bcxqq = bcxguess[bcxguess.rfind('=')+1:bcxguess.rfind(']')]
                        else:
                            bcxqq = bcxguess
                        print(bcxqq)
                        if 'CQ:at' in bcxguess:
                            try:
                                bcmcode = bcxVIPid[str(bcxqq)]
                            except:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:可能您要查找的账号没有与机器人绑定(或许您提供的信息是编程猫ID或者是空?我们目前只接受从QQ的@获取到的QQ号)，咱在自己的数据库找不到您的信息哇QwQ'})
                                #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                                continue
                        else:
                            bcmcode = bcxqq
                        print(bcmcode)
                        #bcxloginfo = json.loads(BCMCreator.association_log_id_local(bcmcode,3), strict=False)
                        bcxloginfo = json.loads(BCMCreator.association_log_id(bcmcode,3), strict=False)
                        #print(bcxloginfo)
                        #if bcxinfo.get("code") == '200':
                        if 'code' in bcxloginfo:
                            #print('True')
                            if bcxloginfo.get("code") == '404':
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:咱没有在服务器数据库找到您要找的人的日志哇，要不问问鱼鱼QwQ?'})
                                #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        else:
                            bxclogmessage = "[CQ:at,qq="+str(qq)+"]\n成功查询到关于此人的日志awa:\n"
                            bxclogmessageline = 1
                            for line in bcxloginfo:
                                #line = demjson.decode(line)
                                bxclogmessage = bxclogmessage + '------第'+str(bxclogmessageline)+'条------\n时间:' + str(line.get('time')) + '\n委员:' + str(line.get("name")) + '\n原因:' + str(line.get('yy')) +'\n'
                                bxclogmessageline = bxclogmessageline + 1
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':bxclogmessage})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#日志):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                elif message[0:6] == '#委员日志 ':
                    try:
                        bcxguess = message[6:len(message)]
                        print(bcxguess)
                        if 'CQ:at' in bcxguess:
                            bcxqq = bcxguess[bcxguess.rfind('=')+1:bcxguess.rfind(']')]
                        else:
                            bcxqq = bcxguess
                        print(bcxqq)
                        if 'CQ:at' in bcxguess:
                            try:
                                bcmcode = bcxVIPid[str(bcxqq)]
                            except:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:可能您要查找的账号没有与机器人绑定(或许您提供的信息是编程猫ID或者是空?我们目前只接受从QQ的@获取到的QQ号)，咱在自己的数据库找不到您的信息哇QwQ'})
                                #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                                continue
                        else:
                            bcmcode = bcxqq
                        print(bcmcode)
                        #bcxloginfo = json.loads(BCMCreator.association_log_uid_local(bcmcode,3), strict=False)
                        bcxloginfo = json.loads(BCMCreator.association_log_uid(bcmcode,3), strict=False)
                        if 'code' in bcxloginfo:
                            if bcxloginfo.get("code") == '404':
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:咱没有在服务器数据库找到您要找的人的日志哇，要不问问鱼鱼QwQ?'})
                                #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        else:
                            bxclogmessage = "[CQ:at,qq="+str(qq)+"]\n成功查询到关于此人的日志awa:\n"
                            bxclogmessageline = 1
                            for line in bcxloginfo:
                                #line = demjson.decode(line)
                                bxclogmessage = bxclogmessage + '------第'+str(bxclogmessageline)+'条------\n时间:' + str(line.get('time')) + '\n委员:' + str(line.get("name")) + '\n原因:' + str(line.get('yy')) +'\n'
                                bxclogmessageline = bxclogmessageline + 1
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':bxclogmessage})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#委员日志):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                elif message[0:5] == '#委员日志':
                    try:
                        bcxguess = message[5:len(message)]
                        print(bcxguess)
                        if 'CQ:at' in bcxguess:
                            bcxqq = bcxguess[bcxguess.rfind('=')+1:bcxguess.rfind(']')]
                        else:
                            bcxqq = bcxguess
                        print(bcxqq)
                        if 'CQ:at' in bcxguess:
                            try:
                                bcmcode = bcxVIPid[str(bcxqq)]
                            except:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:可能您要查找的账号没有与机器人绑定(或许您提供的信息是编程猫ID或者是空?我们目前只接受从QQ的@获取到的QQ号)，咱在自己的数据库找不到您的信息哇QwQ'})
                                #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                                continue
                        else:
                            bcmcode = bcxqq
                        print(bcmcode)
                        #bcxloginfo = json.loads(BCMCreator.association_log_uid_local(bcmcode,3), strict=False)
                        bcxloginfo = json.loads(BCMCreator.association_log_uid(bcmcode,3), strict=False)
                        if 'code' in bcxloginfo:
                            if bcxloginfo.get("code") == '404':
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:咱没有在服务器数据库找到您要找的人的日志哇，要不问问鱼鱼QwQ?'})
                                #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        else:
                            bxclogmessage = "[CQ:at,qq="+str(qq)+"]\n成功查询到关于此人的日志awa:\n"
                            bxclogmessageline = 1
                            for line in bcxloginfo:
                                #line = demjson.decode(line)
                                bxclogmessage = bxclogmessage + '------第'+str(bxclogmessageline)+'条------\n时间:' + str(line.get('time')) + '\n委员:' + str(line.get("name")) + '\n原因:' + str(line.get('yy')) +'}-\n'
                                bxclogmessageline = bxclogmessageline + 1
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':bxclogmessage})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#委员日志):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                elif message[0:5] == '#全局日志':
                    if rev["message_type"] == "group":
                        if cqhttpaccesstoken == '':
                            qqinfojson = json.loads(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&no_cache=true').text, strict=False)
                        else:
                            qqinfojson = json.loads(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&no_cache=true'+'&access_token='+str(cqhttpaccesstoken)).text, strict=False)
                        print('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&access_token='+str(cqhttpaccesstoken))
                        print(qqinfojson)
                        print(str(qqinfojson.get("data").get("role")))
                        if str(qqinfojson.get("data").get("role")) == "member":
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]抱歉，您不是管理员或群主'})
                            continue
                        else:
                            try:
                                #bcxloginfo = json.loads(BCMCreator.association_log_local(5), strict=False)
                                bcxloginfo = json.loads(BCMCreator.association_log(5), strict=False)
                                if 'code' in bcxloginfo:
                                    if bcxloginfo.get("code") == '404':
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:咱没有在服务器数据库找到您要找的人的日志哇，要不问问鱼鱼QwQ?'})
                                        #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                                else:
                                    #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                                    #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                                    bxclogmessage = '\n'
                                    for line in bcxloginfo:
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+ '\n时间:' + str(line.get('time')) +'\n委员:' + str(line.get('name')) +'\n委员编程猫ID:' + str(line.get('id'))  + '\n被执行委员编程猫ID:' + str(line.get('beuid')) + '\n原因:' + str(line.get('yy'))})
                            except BaseException as error:
                                crashlogsave("BCMcreator(#全局日志):"+str(error))
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]查找失败:'+str(error)})
                                send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]该功能只能在群聊使用'})
                elif message[0:5] == '#本周排名' or message[0:6] == '#本周排行榜':
                    if rev["message_type"] == "group":
                        if cqhttpaccesstoken == '':
                            qqinfojson = json.loads(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&no_cache=true').text, strict=False)
                        else:
                            qqinfojson = json.loads(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&no_cache=true'+'&access_token='+str(cqhttpaccesstoken)).text, strict=False)
                        print('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&access_token='+str(cqhttpaccesstoken))
                        print(qqinfojson)
                        print(str(qqinfojson.get("data").get("role")))
                        if str(qqinfojson.get("data").get("role")) == "member":
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]抱歉，您不是管理员或群主'})
                            continue
                        else:
                            #bcxrankjson = BCMCreator.user_workdata7_local()
                            bcxrankjson = BCMCreator.user_workdata7()
                            print(bcxrankjson)
                            #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(bcxrankjson)})
                            bcxrank = json.loads(bcxrankjson)
                            bcxrankmessage = "[CQ:at,qq="+str(qq)+"] "+"[CQ:face,id=147]这是本周的作品排行榜:\n序号.作品名称(作品ID) 分数"
                            bcxrankline = 1
                            for line in bcxrank:
                                if float(line.get("fs")) >= 0.25:
                                    bcxrankdict = str(line.get("id")).split("&")
                                    bcxrankmessage = bcxrankmessage + '\n' + str(bcxrankline) + '.' + str(bcxrankdict[1]) + '(' + str(bcxrankdict[0]) + ') ' + str(line.get("fs"))
                                    bcxrankline = bcxrankline + 1
                                else:
                                    break
                            bcxrankmessage = bcxrankmessage + '\n(以上数据来自前7天的作品投稿数据，仅展示0.25分数及以上的。更多数据请查看https://storage.bcmcreator.cn/Outstandingzp.php (话说这上面有没有你的呢?awa))'
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':bcxrankmessage})
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]该功能只能在群聊使用'})
                elif message[0:8] == '#同步编程猫昵称':
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'开始修改昵称......'})
                    try:
                        try:
                            bcmcode = bcxVIPid[str(qq)]
                        except:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]修改失败:可能您的账号没有与机器人绑定(使用该功能必须绑定机器人，后续可退出登录)，咱在自己的数据库找不到您的信息哇QwQ'})
                            #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                            continue
                        #bcxinfo = json.loads(BCMCreator.user_info_local(bcmcode), strict=False)
                        bcxinfo = json.loads(BCMCreator.user_info(bcmcode), strict=False)
                        if bcxinfo.get("code") == '200':
                            print(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/set_group_card?group_id='+str(sendid)+'&user_id='+str(qq)+'&card='+str(bcxinfo.get("name"))+'-'+str(bcxinfo.get("uid"))+'&access_token='+str(cqhttpaccesstoken)).content)
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=147]修改完成awa:'+str(bcxinfo.get("name"))+'-'+str(bcxinfo.get("uid"))})
                        elif bcxinfo.get("code") == '404':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]修改失败:咱没有在服务器数据库找到您哇，要不问问鱼鱼QwQ?'})
                            #send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]修改失败('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                            send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：('+str(bcxinfo.get('code'))+'):'+str(bcxinfo.get('msg'))})
                    except BaseException as error:
                        crashlogsave("BCMcreator(#同步编程猫昵称):"+str(error))
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]修改失败:'+str(error)})
                        send_msg({'msg_type':str(messagetype),'number':int(superadmin),'msg':'代码执行时发送了错误QAQ：'+str(error)})
                elif message[0:10] == '#查询委员会精神状态' or message[0:10] == '#查询编创协精神状态':
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'Null(?)'})
                elif message[0:9] == '#查询委员精神状态':
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'Null(?)'})
                elif message[0:3] == '#查询' and message[len(message)-4:len(message)] == '精神状态':
                    people = message[3:len(message)-4]
                    if people == '薄荷':
                        if Debug == 1:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'自我升级中...(正在调试)'})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'GOOD'})
                    elif people == '耀西':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq=2659170494]"+'耀西你就歌姬吧，你记住我说的话哦我就站在这个群里骂你就是等你，忍不住。'})
                    elif people == '冷鱼':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'没有眼睛的fish叫什么?叫fsh'})
                    elif people == '小鱼':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'水煮活鱼'})
                    elif people == '绵羊':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'Beep Beep,Im sheep.I say Beep Beep im sheep'})
                    elif people == 'array' or people == '矮睿':
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'你所热爱的，就是你的生活'})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'新时代的矮睿吃冷鱼！'})
                    elif people == '斯人':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'斯'})
                    elif people == '技术狗':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'if codemao == "编程猫":\n    codedog = "编程狗"'})
                    elif people == '热猫':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'建议搭配冷鱼食用'})
                    elif people == '冷鱼':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'建议搭配热猫食用'})
                    elif people == '星舰' or people == '星舰earth' or people == 'earth':
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'我新买的航母怎么飞了?'})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'星舰earth，为战而生，无所畏惧！！！'})
                    elif people == 'ScratchMaster' or people == "SM" or people == "sm" or people == 'Sm' or people == "scratchmaster":
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'https://github.com/LLK/scratch-gui/tree/master'})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'ScratchMaster曰：我的名字是ScratchMaster，原本是一名全国知名的高中生名侦探，不幸的是不久之前被不明组织强灌毒药…… 而变成了江户川sm！我人虽然变小了，头脑还是原来的名侦探。不管发生什么事件，我相信真相只有一个！不对，凶手如果是他，那他的不在场证明···对了！呵，我懂了，原来是这样！'})
                    elif people == '企鹅':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'企...企...企鹅是谁?QwQ'})
                    elif people == '鸭':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'嘎awa'})
                    elif people == '我' or people == '我的':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'我?我是谁?XwX'})
                    elif people == '冷鱼与热猫':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'哇！金色传说！！！'})
                    elif people == '冷鱼吃热猫':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'小鱼吃大猫awa'})
                    elif people == '热猫吃冷鱼':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'啊，真香哎呀'})
                    elif people == '技术喵' or people == '技术猫':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'Is Coding...'})
                    elif people == '派大星':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'艺术就是派大星!!!'})
                    elif people == '赖纸':
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'查询错误XwX:请求超时'})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'尬聊的屑'})
                    elif people == '乔治':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'佩奇呢?awa'})
                    elif people == '天边的生活':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'蓝！好蓝啊！awa'})
                    elif people == '霜雪冬竹':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'好吃吗?awa'})
                    elif people == 'Null':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'Null'})
                    elif people == '阿兹卡班' or people == '阿兹卡班毕业生':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'哪个班的学生？上课竟然玩手机！？'})
                    elif people == "工人" or people == "nomand" or people == "Nomand":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"兰州铁路监管局投诉举报联系方式：\n地址：甘肃省兰州市城关区和政路129号　邮编：730000\n举报电话：0931-4975119 0931-4975183\n传真：0931-4975109\n电子邮箱：lanzhoudiquju@nra.gov.cn\n\n女士们，先生们，欢迎选乘动车组列车!本次列车由 中川机场 开往 兰州 方向。请不要携带危险物品乘车，动车组列车全程对号入座。\nLadies and gentlemen, welcome aboard the high-speed train. This high-speed train departing from Zhongchuanjichang Station is headed for Lanzhou station. Dangerous items are not allowed within the railway promises. Please be seated by numbers corresponding to the ticket throughout the journey. \n女士们，先生们，严禁在动车组列车任何区域内吸烟。根据《铁路安全管理条例》等法律法规，在动车组列车上吸烟需承担法律责任。\nLadies and gentlemen, this is a non-smoking train. According to the railway security management regulations and relevant laws, the smoker shall assume legal responsibility. Please do not smoke on board. Thanks for your cooperation.\n兰州铁路局环西部火车游祝您旅途愉快！\nLanzhou Railway Bureau's train tour around the West wish you a pleasant journey!"})
                    elif people == '安':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'整理遗容遗表'})
                    elif  people == '贝奇':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'我要喝电气水!!!'})
                    elif people == '1086':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'勇敢86，不怕困难!'})
                    elif people == '蔡徐坤' or people == '坤坤':
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'只因你太美'})
                    elif people == "小柠檬":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'被酸倒呜！XwX'})
                    elif people == "涂卡":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'嗷呜!'})
                    elif people == "当当":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'口当!'})
                    elif people == "狰豹":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'嘿嘿！嗷呜！'})
                    elif people == "鸭子":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'这个鸭子真咸！qwq'})
                    elif people == "小果果":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'滑稽树上滑稽果，滑稽树下你和我awa'})
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'啊！是空的XwX(或许。。。可以尝试申请一下？)'})
                elif message[0:9] == "#开启聊天室收发信" or message[0:8] == "#开启群聊收发信" or message[0:10] == "#开启聊天室收发消息" or message[0:9] == "#开启群聊收发消息" or message[0:7] == "#开启收发消息" or message[0:6] == "#开启收发信"  or message[0:10] == "#开启聊天群收发消息":
                    if rev["message_type"] == "group":
                        '''
                        if cqhttpaccesstoken == '':
                            qqinfojson = json.loads(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&no_cache=true').text, strict=False)
                        else:
                            qqinfojson = json.loads(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&no_cache=true'+'&access_token='+str(cqhttpaccesstoken)).text, strict=False)
                        print('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&access_token='+str(cqhttpaccesstoken))
                        print(qqinfojson)
                        print(str(qqinfojson.get("data").get("role")))
                        if str(qqinfojson.get("data").get("role")) == "member" and str(sendid) != "2659170494":
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]抱歉，您不是管理员或群主'})
                            continue
                        else:
                        '''
                        if str(ChatMessageAllow) == "1":
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]该功能已经开启'})
                        else:
                            ChatMessageAllow == 1
                            exec(f"global ChatMessageAllow;ChatMessageAllow = 1")
                            save_save()
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'开启成功'})
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]该功能只能在群聊使用'})
                elif message[0:9] == "#关闭聊天室收发信" or message[0:8] == "#关闭群聊收发信" or message[0:10] == "#关闭聊天室收发信息" or message[0:9] == "#关闭群聊收发消息" or message[0:7] == "#关闭收发消息" or message[0:6] == "#关闭收发信" or message[0:len(message)] == r"#[CQ:at,qq="+QQID+r"]" or message[0:len(message)] == r"#[CQ:at,qq="+QQID+r"] " or message[0:12+len(QQID)] == r"#[CQ:at,qq="+QQID+r"]" or message[0:13+len(QQID)] == r"#[CQ:at,qq="+QQID+r"] "  or message[0:10] == "#关闭聊天群收发消息" or str(message).strip() == str(r"#[CQ:at,qq="+QQID+r"] ") or str(message).strip() == str(r"#[CQ:at,qq="+QQID+r"]"):
                    if rev["message_type"] == "group":
                        '''
                        if cqhttpaccesstoken == '':
                            qqinfojson = json.loads(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&no_cache=true').text, strict=False)
                        else:
                            qqinfojson = json.loads(requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&no_cache=true'+'&access_token='+str(cqhttpaccesstoken)).text, strict=False)
                        print('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/get_group_member_info?group_id='+str(sendid)+'&user_id='+str(qq)+'&access_token='+str(cqhttpaccesstoken))
                        print(qqinfojson)
                        print(str(qqinfojson.get("data").get("role")))
                        if str(qqinfojson.get("data").get("role")) == "member" and str(sendid) != "2659170494":
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]抱歉，您不是管理员或群主'})
                            continue
                        else:
                        '''
                        if str(ChatMessageAllow) == "0":
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]该功能已经关闭'})
                        else:
                            ChatMessageAllow == 0
                            exec(f"global ChatMessageAllow;ChatMessageAllow = 0")
                            save_save()
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'关闭成功'})
                    else:
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]"+'[CQ:face,id=9]该功能只能在群聊使用'})
                elif message[0:7] == '#展示最新文章':
                    bcxblogtext = "---编创协最新文章---\n以下是论坛目前最新的文章哇"
                    #bcxblogjson = json.loads(BCMCreator.getBlog_local())
                    bcxblogjson = json.loads(BCMCreator.getBlog())
                    for blogjson in bcxblogjson:
                        bcxblogtext = bcxblogtext + "\n[CQ:face,id=57]标题："+str(blogjson.get("name"))+"\n简介："
                        if len(str(blogjson.get("js"))) > 20:
                            bcxblogjs = str(blogjson.get("js"))[0:20] + "..."
                        else:
                            bcxblogjs = str(blogjson.get("js"))
                        bcxblogtext = bcxblogtext + bcxblogjs +"\n作者："+str(blogjson.get("user")) + "\n观看量："+str(blogjson.get("fw"))+"\n标签："+str(blogjson.get("gjz"))+"\n时间："+str(blogjson.get("time")) + "\n帖子链接：https://shequ.bcmcreator.cn/blogview.php?id="+str(blogjson.get("md"))
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]\n"+str(bcxblogtext)})
                elif message[0:5] == '#临时文件':
                    pass
                elif message[0:3] == '#菜单':
                    bcxmenu = '---编创协机器人菜单---'
                    for a in bcxmenulist:
                        bcxmenu = bcxmenu + '\n[CQ:face,id=74]' + str(a)
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]\n"+str(bcxmenu)})
                elif message[0:len(BotName)+1] == BotName+',' or message[0:len(BotName)+1] == BotName+'，' or message[0:len("[CQ:at,qq="+QQID+"]")+2] == "[CQ:at,qq="+QQID+"] "+"，" or message[0:len("[CQ:at,qq="+QQID+"]")+2] == "[CQ:at,qq="+QQID+"] "+","or message[0:len("[CQ:at,qq="+QQID+"]")+1] == "[CQ:at,qq="+QQID+"]"+"，" or message[0:len("[CQ:at,qq="+QQID+"]")+1] == "[CQ:at,qq="+QQID+"]"+",":
                    if str(Debug) == '1':
                        if rev["message_type"] == "private":
                            if str(sendid) != str(DebugQQID):
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+r'/Debug.jpg]'})
                                continue
                        elif rev["message_type"] == "group":
                            if str(sendid) != str(DebugGroupID):
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+r'/Debug.jpg]'})
                                continue
                        else:
                            continue
                    if message[0:len("[CQ:at,qq="+QQID+"]")+1] == "[CQ:at,qq="+QQID+"] ":
                        messagecommand = message[len("[CQ:at,qq="+QQID+"]")+2:len(message)]
                    elif message[0:len("[CQ:at,qq="+QQID+"]")] == "[CQ:at,qq="+QQID+"]":
                        messagecommand = message[len("[CQ:at,qq="+QQID+"]")+1:len(message)]
                    else:
                        messagecommand = message[len(BotName)+1:len(message)]
                    print(messagecommand)
                    if str(qq) in privateblacklist or str(qq) in groupblacklist or str(sendid) in privateblacklist or str(sendid) in groupblacklist:
                        try:
                            send_msg({'msg_type':'private','number':int(superadmin),'msg':'收到来自'+str(sendid)+'(在黑名单内)的'+str(messagetype)+'消息：'+str(message)})
                            continue
                        except BaseException as error:
                            crashlogsave("黑名单消息转发管理:"+str(error))
                            send_msg({'msg_type':'private','number':int(superadmin),'msg':'收到'+str(messagetype)+'消息但发送了错误QAQ：'+str(error)})
                            continue
                        message = ""
                        messagecommand = ""
                    if messagecommand[0:5] == '加入黑名单':
                        if sendid in adminQQ or sendid == superadmin:
                            if '到人' in messagecommand or '到群' in messagecommand:
                                if '群' in messagecommand:
                                    groupblacklist.append(str(messagecommand[5:messagecommand.rfind('到')]))
                                    save_save()
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+int(sendid)+']添加成功awa'})
                                elif '人' in messagecommand:
                                    privateblacklist.append(str(messagecommand[5:messagecommand.rfind('到')]))
                                    save_save()
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+int(sendid)+']添加成功awa'})
                            else:
                                print('加入黑名单失败:没有找到对应关键词')
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+int(sendid)+']加入黑名单失败:没有找到关键词QwQ'})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+int(sendid)+']你不是管理员QwQ'})
                    if messagecommand[0:5] == '删除黑名单':
                        if sendid in adminQQ or sendid == superadmin:
                            if '到人' in messagecommand or '到群' in messagecommand:
                                if '群' in messagecommand:
                                    groupblacklist.remove(str(messagecommand[5:messagecommand.rfind('到')]))
                                    save_save()
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+int(sendid)+']添加成功awa'})
                                elif '人' in messagecommand:
                                    privateblacklist.remove(str(messagecommand[5:messagecommand.rfind('到')]))
                                    save_save()
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+int(sendid)+']添加成功awa'})
                            else:
                                print('删除黑名单失败:没有找到对应关键词')
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+int(sendid)+']加入黑名单失败:没有找到关键词QwQ'})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'[CQ:at,qq='+int(sendid)+']你不是管理员QwQ'})
                    if messagecommand[0:4] == '发送消息':
                        sendmessageidlist = []
                        if str(qq) in adminQQ or str(qq) == superadmin :
                            if '到' in messagecommand:
                                if '群' in messagecommand:
                                    try:
                                        send_msg({'msg_type':'group','number':int(messagecommand[messagecommand.rfind('到')+1:messagecommand.rfind('群')]),'msg':str(messagecommand[4:messagecommand.rfind('到')])})
                                    except BaseException as error:
                                        crashlogsave("发送消息功能(到群):"+str(error))
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                        print('所有异常的基类：'+str(error))
                                        continue
                                elif '人' in messagecommand:
                                    try:
                                        send_msg({'msg_type':'private','number':int(messagecommand[messagecommand.rfind('到')+1:messagecommand.rfind('人')]),'msg':str(messagecommand[4:messagecommand.rfind('到')])})
                                    except BaseException as error:
                                        crashlogsave("发送消息功能(到人):"+str(error))
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                        print('所有异常的基类：'+str(error))
                                        continue
                                else:
                                    try:
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(messagecommand[4:len(messagecommand)])})
                                    except BaseException as error:
                                        crashlogsave("发送消息功能(到):"+str(error))
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                        print('所有异常的基类：'+str(error))
                                        continue
                            else:
                                try:
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(messagecommand[4:len(messagecommand)])})
                                except BaseException as error:
                                    crashlogsave("发送消息功能:"+str(error))
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                    print('所有异常的基类：'+str(error))
                                    continue
                        else:
                            try:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]您不是管理员QwQ"}) 
                            except BaseException as error:
                                crashlogsave("发送消息功能(非管理):"+str(error))
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,出错了QAQ："+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                print('所有异常的基类：'+str(error))
                                continue
                    if  messagecommand[0:2] == "找找":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"],[CQ:face,id=12]找找功能已分为两个功能，分别是'涂鸦找找'(默认找找)、'云绒找找'和'绒狸找找'。具体请对我说'"+str(BotName)+",菜单'查看功能详情吧[CQ:face,id=12]"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif  messagecommand[0:4] == "涂鸦找找":
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]抱歉哇，最近涂鸦宇宙正在维护升级，这个功能暂时不能用QwQ"}) 
                        #continue
                        findfriend = messagecommand[4:len(messagecommand)]
                        findfriendjson = demjson.decode(WebFurApi.tuyaV3find_name(TuYaApiID,TuYaApiKey,findfriend))
                        if findfriendjson.get("code") == 0:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=147]"+str(findfriendjson.get('data').get('name'))+'（ID：'+str(findfriendjson.get('data').get('id'))+'）'+str('\n')+"[CQ:face,id=144]破壳："+str(findfriendjson.get('data').get('birthday'))+str('\n')+"[CQ:face,id=75]家乡："+str(findfriendjson.get('data').get("hometown"))+str('\n')+"[CQ:face,id=185]物种："+str(findfriendjson.get('data').get("animal"))+str('\n')+"[CQ:face,id=12]性格："+str(findfriendjson.get('data').get("cha"))+str('\n')+"[CQ:face,id=66]喜欢："+str(findfriendjson.get('data').get("likes"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(findfriendjson.get('data').get("intro"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            """
                            tuyaimg = WebFurApi.tuyaV3find_img_old(TuYaApiID,TuYaApiKey,findfriend)
                            try:
                                json.loads(tuyaimg)
                                imgisjson = 1
                            except:
                                imgisjson = 0
                            if imgisjson == 1:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,发送图片失败了qwq"})
                            else:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':f"[CQ:image,file=file:///{tuyaimg}]"})
                            """
                            if findfriend != "":
                                tuyaimg = WebFurApi.tuyaV3find_img_new(TuYaApiID,TuYaApiKey,findfriend,0) 
                            else:
                                tuyaimg = WebFurApi.tuyaV3find_img_new(TuYaApiID,TuYaApiKey,str(findfriendjson.get('data').get('name')),0) 
                            print(tuyaimg)
                            try:
                                tuyaimgjson = json.loads(tuyaimg)
                                try:
                                    tuyaimgjsonapijson = json.loads(tuyaimgjson.get("apijson"))
                                    if str(tuyaimgjsonapijson.get("code")) == "1002":
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=106]呜呜，找找把照片找丢了欸QwQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                    else:
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:(找找找图片把问题找出来了XwX)"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                except:
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:(找找找图片把问题找出来了XwX)"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            except:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':f"[CQ:image,file=file:///{tuyaimg}]"})
                                #pass
                        elif findfriendjson.get("code") == 1002:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=106]呜呜，我好像没有找到他呢，该不会是没来过？(或者叫找找找找?)QwQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+str(findfriendjson.get("code"))+"):"+findfriendjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        '''
                        findfriend = messagecommand[4:len(messagecommand)]
                        findfriendjson = demjson.decode(WebFurApi.tuyaV1findname(findfriend))
                        if findfriendjson.get("code") == 200:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=147]"+str(findfriendjson.get('data').get('name'))+'（ID：'+str(findfriendjson.get('data').get('id'))+'）'+str('\n')+"[CQ:face,id=144]破壳："+str(findfriendjson.get('data').get('birthday'))+str('\n')+"[CQ:face,id=75]家乡："+str(findfriendjson.get('data').get("hometown"))+str('\n')+"[CQ:face,id=159]物种："+str(findfriendjson.get('data').get("animal"))+str('\n')+"[CQ:face,id=12]性格："+str(findfriendjson.get('data').get("character"))+str('\n')+"[CQ:face,id=66]喜欢："+str(findfriendjson.get('data').get("likes"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(findfriendjson.get('data').get("intro"))+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=https://duo-api.turka.cn/tuyafriends/img/"+str(findfriendjson.get('data').get('imgid'))+".png]"})
                        elif findfriendjson.get("code") == -10:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=106]呜呜，我好像没有找到他呢，该不会是没来过？QwQ"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+findfriendjson.get("code")+"):"+findfriendjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        '''
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
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"]抱歉哇，今日早报的API原作者貌似放起来这个项目(现作者博客和API均无法访问)。所以该功能暂停使用QwQ"}) 
                        #continue
                        sixtysjson = json.loads(WebMediaApi.Sixty03C3())
                        if sixtysjson.get("code") == 200:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜,这是今天的早报"+str('\n')+"[CQ:image,file="+str(sixtysjson.get('imageUrl'))+"]"+str('\n')+"当前早报的时间:"+sixtysjson.get("datatime")+"."+str('\n')+"(想要API接口吗？去GreenYoshi的杂货库( http://wanghan123456.ysepan.com/ )的文档文件夹上看看吧，不定时更新)"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+sixtysjson.get("code")+"):"+sixtysjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif  messagecommand[0:5] == "绒狸来只毛":
                        if furauthKey == '' or furauthqq == '':
                            microtailjson = json.loads(WebFurApi.microtailV1random())
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
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+str(microtailjson.get("code"))+")："+microtailjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                        else:
                            microtailjson = json.loads(WebFurApi.microtailV2random(furauthqq,int(time.time()),furauthKey))
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
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+str(microtailjson.get("code"))+")："+microtailjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif messagecommand[0:4] == "绒狸找找":
                        if furauthKey == '' and furauthqq == '':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,主人还没有给我必要的信息。咱没办法查找qwq"+"\n-------------------"+str('\n')+MintBotVersion})
                        else:
                            furfindname = messagecommand[4:len(messagecommand)]
                            print(furfindname)
                            microtailjson = json.loads(WebFurApi.microtailV2find_name(str(furauthqq),str(int(time.time())),str(furauthKey),str(furfindname)))
                            print(microtailjson)
                            if microtailjson.get("code") == 200:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜！有请毛毛："+str(microtailjson.get("data").get("name"))+"（ID："+str(microtailjson.get("data").get("id"))+"）"+str("\n")+"内容来自：绒狸MicroTail"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                                microtailimg = requests.get(microtailjson.get('data').get("url"))
                                microtailfiletype = filetype.guess(microtailimg.content)
                                print(microtailimg)
                                with open(os.getcwd()+"\microtailtmp."+microtailfiletype.extension,'wb') as f:
                                    f.write(microtailimg.content)
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\microtailtmp."+microtailfiletype.extension+"]"})
                            elif microtailjson.get("code") == 404:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]呜呜,没有找到这只兽兽哇"})
                            else:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+str(microtailjson.get("code"))+")："+microtailjson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif messagecommand[0:5] == "云绒来只毛":
                        furruijson = json.loads(WebFurApi.furruiV2random())
                        if str(furruijson.get("code")) == '20900':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜！有请毛毛："+str(furruijson.get("picture").get("name"))+str("\n")+"内容来自：兽云祭"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+str(WebFurApi.furruiV2get_img(furruijson.get("picture").get("picture")))+"]"})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+furruijson.get("code")+")："+furruijson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif messagecommand[0:4] == "云绒找找":
                        furruiname = messagecommand[4:len(messagecommand)]
                        furruijson = json.loads(WebFurApi.furruiV2random_somebody(furruiname,""))
                        if str(furruijson.get("code")) == '20900':
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=12]嗷呜！有请毛毛："+str(furruijson.get("picture").get("name"))+str("\n")+"内容来自：兽云祭"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+str(WebFurApi.furruiV2get_img(furruijson.get("picture").get("picture")))+"]"})
                        else:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败了qwq:("+furruijson.get("code")+")："+furruijson.get("msg")+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                    elif messagecommand[0:3] == "来只毛":
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"],[CQ:face,id=12]来只毛功能已分为两个功能，分别是'绒狸来只毛'(默认来只毛)和'云绒来只毛'。具体请对我说'"+str(BotName)+",菜单'查看功能详情吧[CQ:face,id=12]"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
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
                        searchweatherjson = json.loads(WebMediaApi.QweatherV2FindCity(weatherKEY,messagecommand[0:len(messagecommand)-2]))
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
                                weatherjson = json.loads(WebMediaApi.QweatherV7Today(weatherKEY,swid))
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
                                                swmessage = swmessage +str(swlistlen) + '：' + str(swjson.get("adm1")) + "，" + str(swjson.get("adm2")) + "，" + str(swjson.get("name")) + "(ID：" + str(swjson.get("id")) + ")" +'\n'
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
                                                                                weatherjson = json.loads(WebMediaApi.QweatherV7Today(weatherKEY,swid))
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
                                                                    elif message[0:len(BotName)+5] == BotName+"，停止操作" or message[0:len(BotName)+5] == BotName+",停止操作":
                                                                        try:
                                                                            swlistlen=swlistlen+1
                                                                            print(str(searchweatherQQ)+"已中止")
                                                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchweatherQQ)+"][CQ:face,id=9]呜呜,指令已被终止qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                            wmsucessful = 1
                                                                            break
                                                                        except:
                                                                            swlistlen=swlistlen+1
                                                                            print(str(searchweatherQQ)+"已中止")
                                                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"已终止操作qwq"})
                                                                            wmsucessful = 1
                                                                            break
                                                                    elif BotName in message:
                                                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,目前服务被"+searchweatherQQ+"占用中qwq(任何人都可以回复'"+BotName+"，停止操作'中止执行人操作)"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                                        messageRefresh = 0
                                                                        continue
                                                                    else:
                                                                        continue
                                            print('循环回复已结束')
                                            break
                                    except Exception as error:
                                        crashlogsave("搜索天气:"+str(error))
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
                            if menulistline[0:3] == "---":
                                menumessage = menumessage + str("\n")+menulistline
                            elif menulistline[0:1].isdigit() == True:
                                menumessage = menumessage + str("\n")+menulistline
                            else:
                                menumessage = menumessage + str("\n")+'[CQ:face,id=66]'+menulistline
                        menumessage = menumessage + str("\n")+"-------------------"+str("\n")+MintBotVersion
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':menumessage})
                    elif messagecommand[0:2] == '找书':
                        bookname = messagecommand[2:len(messagecommand)]
                        if json.loads(WebMediaApi.ZlibV1OK(ZlibraryURL)).get("success") == 1:
                            try:
                                while Zliblogin == 0:
                                    if Zliblogin == 0:
                                        Zlibloginrequeststext = WebMediaApi.ZlibV1Login(ZlibraryURL,ZlibUserEmail,ZlibPassword)
                                        Zlibloginjson = json.loads(Zlibloginrequeststext)
                                        print(Zlibloginjson)
                                        if Zlibloginjson.get('success') == 1:   
                                            Zliblogincookies = Zlibloginjson.get("cookies")
                                            print(Zliblogincookies)
                                            ZlibUser = Zlibloginjson.get("data").get('user')
                                            print(ZlibUser) 
                                            ZlibUsername = ZlibUser.get("data").get('name')
                                            print(ZlibUsername)
                                            ZlibUserID = ZlibUser.get("data").get('id')
                                            print(ZlibUserID)
                                            ZlibUserkey = ZlibUser.get("data").get('remix_userkey')
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
                                    booksearchlistjson = json.loads(WebMediaApi.ZlibV1FindBookName(ZlibraryURL,bookname)).get("books")
                                    booksearchlist = []
                                    booksearchIDlist = []
                                    booksearchnamelist = []
                                    booksearchcoverlist = []
                                    booksearchextensionlist = []
                                    booksearchlanguagelist = []
                                    booksearchauthorlist = []
                                    booksearchhashlist = []
                                    booksearchdescriptionlist = []
                                    #print(bookname)
                                    for bsline in booksearchlistjson:
                                        booksearchlist.append(bsline)
                                        print(bsline)
                                        booksearchIDlist.append(bsline.get("id"))
                                        print(bsline.get("id"))
                                        booksearchnamelist.append(bsline.get("title"))
                                        print(bsline.get("title"))
                                        booksearchcoverlist.append(bsline.get("cover"))
                                        booksearchextensionlist.append(bsline.get("extension"))
                                        booksearchlanguagelist.append(bsline.get("language"))
                                        booksearchauthorlist.append(bsline.get("author"))
                                        booksearchhashlist.append(bsline.get("hash"))
                                        print(bsline.get("hash"))
                                        booksearchdescriptionlist.append(bsline.get("description"))
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(booksearchnamelist)})
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(booksearchIDlist)})
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(booksearchhashlist)})
                                elif Zliblogin == 2:
                                    Zliblogin = 0
                                else:
                                    print('登录失败：未知错误')
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,登录失败QAQ:未知错误"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                    Zliblogin = 0
                            except BaseException as error:
                                print('失败了QAQ：'+str(error))
                                crashlogsave("Zlib搜书:"+str(error))
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,失败QAQ:"+str(error)+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                continue
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
                            elif messagecommand[0:5] == '网易云音乐':
                                songtype = 'netease'
                                songname = messagecommand[7:len(messagecommand)]
                            elif messagecommand[0:4] == 'QQ音乐' or messagecommand[0:4] == 'qq音乐':
                                songtype = 'qq'
                                songname = messagecommand[6:len(messagecommand)]
                            elif messagecommand[0:2] == '酷狗':
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜，酷狗音乐因为API和酷狗服务器屏蔽的原因暂时无法使用qwq"})
                                continue
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
                                                                        crashlogsave("音乐搜索:(QQ音乐使用ffmpeg转换格式时发生的错误)"+str(error))
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
                                                    elif message[0:len(BotName)+5] == BotName+"，停止操作" or message[0:len(BotName)+5] == BotName+",停止操作":
                                                        try:
                                                            print(str(searchsongQQ)+"已中止")
                                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(searchsongQQ)+"][CQ:face,id=9]呜呜,指令已被终止qwq"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                            messagescucess = 1
                                                            messageRefresh = 0
                                                            break
                                                        except:
                                                            print(str(searchsongQQ)+"已中止")
                                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"已终止操作qwq"})
                                                            messagescucess = 1
                                                            messageRefresh = 0
                                                            break
                                                    elif BotName in message:
                                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:face,id=9]呜呜,目前服务被"+searchsongQQ+"占用中qwq(任何人都可以回复'"+BotName+"，停止操作'中止执行人操作)"+str('\n')+"-------------------"+str('\n')+MintBotVersion})
                                                        messageRefresh = 0
                                                        continue
                                                    else:
                                                        continue
                                            else:
                                                print('404')
                                        except BaseException as error:
                                            print('500')
                                            crashlogsave("音乐搜索:"+str(error))
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
                    elif messagecommand[0:4] == "赞助名单":
                        print("有人询问赞助的事哇!XwX")
                        zanzhumessage = "[CQ:at,qq="+str(qq)+']\n[CQ:face,id=12]嗷呜，这是机器人从运营以来收到过的赞助金额哇:'
                        for name in zanzhurenlist:
                            zanzhumessage += f'\n[CQ:face,id=147]{name}'
                        zanzhumessage += f'\n[CQ:face,id=144]首先很感谢大家的支持哇，从刚开始运营原本是受到涂鸦宇宙的启发(包括命令，在此纪念一下(20221002停运qwq))，并以日常使用方向为目标走的。并不使用网上一些第三方娱乐机器人和插件。起初是用OICQ+Clickteam Fusion制作成的，后来由于架构太乱且太多bug。再加上OICQ后续不支持HTTP了，之后改用go-cqhttp+python了。由于是初学所以没用nonebot等需要装插件的(那时服务器装不起XwX)，所以一路都是看教程和不断调试最终走到今天的qwq。直到今天，咱都没有主动让别人赞助，甚至增加赞助才能用的功能。因为那样做的话就违背了我的初心(再者机器人没什么人用，且有的比我优秀多了)XwX，后续也在Github和Gitee上开源了部分代码(但是很久没更新了XwX)。也只是为了引起一些人的注意(但是写的是真的乱XwX)。不过上述人员能够帮助咱发展下去，真的很感谢哇(但咱又没有什么回报XwX)。也祝大家能像往常一样，开开心心就好了awa(本赞助表更新时间为{zanzhutime})'
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':zanzhumessage})
                    elif messagecommand[0:1] == '丢' or messagecommand[0:1] == '丟':
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，这个功能的网站没有经过备案，无法访问QwQ"})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，这个功能的API商跑路了，目前想办法自己移植QwQ"})
                        continue
                        if messagecommand[1:2] == '我':
                            MoId = qq
                        elif 'CQ:at' in messagecommand:
                            MoId = messagecommand[messagecommand.rfind('=')+1:messagecommand.rfind(']')]
                        else:
                            MoId = messagecommand[1 :len(messagecommand)]
                        print(MoId)
                        DiuApiUrl = 'http://api.1il1.com/api/tupian/diu.php?qq='+str(MoId)
                        print(DiuApiUrl)
                        os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                        Diufile = requests.get(DiuApiUrl)
                        print(str(filetype.guess(Diufile.content)))
                        Diufiletype = filetype.guess(Diufile.content).extension
                        print(Diufiletype)
                        with open(os.getcwd()+"\Diuimage."+Diufiletype,'wb') as f:
                            f.write(Diufile.content)
                        print('Sucuessful')
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\Diuimage."+Diufiletype+"]"})
                    elif messagecommand[0:1] == '赞':
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，这个功能的网站没有经过备案，无法访问QwQ"})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，这个功能的API商跑路了，目前想办法自己移植QwQ"})
                        continue
                        if messagecommand[1:2] == '我':
                            MoId = qq
                        elif 'CQ:at' in messagecommand:
                            MoId = messagecommand[messagecommand.rfind('=')+1:messagecommand.rfind(']')]
                        else:
                            MoId = messagecommand[1:len(messagecommand)]
                        print(MoId)
                        ZanApiUrl = 'http://api.1il1.com/api/tupian/zan.php?qq='+str(MoId)
                        print(ZanApiUrl)
                        os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                        Zanfile = requests.get(ZanApiUrl)
                        print(str(filetype.guess(Zanfile.content)))
                        Zanfiletype = filetype.guess(Zanfile.content).extension
                        print(Zanfiletype)
                        with open(os.getcwd()+"\Zanimage."+Zanfiletype,'wb') as f:
                            f.write(Zanfile.content)
                        print('Sucuessful')
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\Zanimage."+Zanfiletype+"]"})
                    elif messagecommand[0:1] == '爬':
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，这个功能的网站没有经过备案，无法访问QwQ"})
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，这个功能的API商跑路了，目前想办法自己移植QwQ"})
                        continue
                        if str(rev["group_id"]) == "": #限制哪些群不能用
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，该群已禁用该功能"})
                            continue
                        if messagecommand[1:2] == '我':
                            MoId = qq
                        elif 'CQ:at' in messagecommand:
                            MoId = messagecommand[messagecommand.rfind('=')+1:messagecommand.rfind(']')]
                        else:
                            MoId = messagecommand[1:len(messagecommand)]
                        print(MoId)
                        PaApiUrl = 'http://api.1il1.com/api/tupian/pa.php?qq='+str(MoId)
                        print(PaApiUrl)
                        os.chdir(r"C:\\Users\Administrator\.go-cqhttp")
                        Pafile = requests.get(PaApiUrl)
                        print(str(filetype.guess(Pafile.content)))
                        Pafiletype = filetype.guess(Pafile.content).extension
                        print(Pafiletype)
                        with open(os.getcwd()+"\Paimage."+Pafiletype,'wb') as f:
                            f.write(Pafile.content)
                        print('Sucuessful')
                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:image,file=file:///"+os.getcwd()+"\Paimage."+Pafiletype+"]"})
                    elif messagecommand[0:2] == '摸摸':
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，摸摸功能因为API维护而暂时停用QwQ"})
                        #continue
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
                        MoApiul = 'https://api.wer.plus/api/ruad?url='+ str(urllib.parse.quote(MoQQimagegetJson.get('imgurl')))
                        #MoApiul = 'http://api.wer.plus:8080/api/ruad?url=' + str(urllib.parse.quote(MoQQimagegetJson.get('imgurl'))) + '&token=' + str(onemingKey)
                        #MoApiul = 'http://101.35.149.229:8080/api/ruad?url=' + str(urllib.parse.quote(MoQQimagegetJson.get('imgurl'))) + '&token=' + str(onemingKey)
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
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+"][CQ:face,id=9]抱歉，摸鱼日历因为不稳定而暂时停用QwQ"})
                        #continue
                        #def MoYuDayDef(messagetype,sendid,qq):
                            #MoYuUrl = 'https://api.vvhan.com/api/moyu?type=json'
                            #MoYuJsonGet = requests.get(MoYuUrl).text
                            #MoYuJson = demjson.decode(MoYuJsonGet)
                            #MoYuFile = requests.get(MoYuJson.get("url"))
                            #MoYuFileType = filetype.guess(MoYuFile.content).extension
                            #with open(os.getcwd()+"\MoYuimage."+MoYuFileType,'wb') as f:
                                #f.write(MoYuFile.content)
                            #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':f"[CQ:at,qq={qq}][CQ:face,id=12]摸鱼时间~~"+str("\n")+"[CQ:image,file=file:///"+os.getcwd()+"\MoYuimage."+MoYuFileType+"]"})
                        #threading.start_new_thread(MoYuDayDef)
                        for moyu in range(1):
                            moyu_time = threading.Thread(target=MoYuDayDef(messagetype,sendid,qq))
                            moyu_time.start()
                        print("创建新线程完成")
                    elif messagecommand[0:4] == '沙盒分析':
                        continue
                        #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':'请发送文件:'})
                        #filesearch = 1
                        #while filesearch == 0:
                            #continue
                    elif messagecommand[0:4] == '网络天才':
                        continue
                    elif messagecommand[0:4] == '马造找找':
                        id = messagecommand[4:len(messagecommand)]
                        if id == "":
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']咕，您没有输入任何的ID欸qwq'})
                        elif len(id) != 9:
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']咕，您输入ID不等于9位数欸，如果您的ID有"-"符号的话请把它去掉qwq'})
                        else:
                            #原理教程视频链接:https://www.bilibili.com/video/BV1UY4y1W7eX
                            id.upper()
                            if "A" in id or "Z" in id or "I" in id or "O" in id or "U" in id or "E" in id:
                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']呜!你乱输的吧!!!薄荷解密ID也是挺幸苦的QAQ(所给的ID不能有A、Z、I、O、U、E字母)'})
                            else:
                                SMM2ID30 = "0123456789BCDFGHJKLMNPQRSTVWXY"
                                SMM2ID30List = []
                                SMM2ID30ListLine = 0
                                SMM2ID10 = 0
                                SMM2ID10List = []
                                SMM2IDSplitList = []
                                for get in id:
                                    SMM2IDSplitList.append(get)
                                #print(SMM2IDSplitList)
                                for get in SMM2IDSplitList:
                                    SMM2ID30List.append(SMM2ID30.find(get))
                                #print(SMM2ID30List)
                                for get in SMM2ID30List:
                                    SMM2ID10List.append(int(int(get)*30**SMM2ID30ListLine))
                                    SMM2ID30ListLine += 1
                                #print(SMM2ID10List)
                                for get in SMM2ID10List:
                                    SMM2ID10 += int(get)
                                #print(SMM2ID10)
                                SMM2ID2 = bin(SMM2ID10)
                                #print(SMM2ID2)
                                #print(len(str(SMM2ID2)[2:len(str(SMM2ID2))]))
                                if len(str(SMM2ID2)[2:len(str(SMM2ID2))]) != 44:
                                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']呜XwX!!!ID解密失败(所解密的二进制不是44位的)'})
                                else:
                                    SMM2ID2Str = str(SMM2ID2)[2:len(str(SMM2ID2))]
                                    SMM2IDA = SMM2ID2Str[0:4]
                                    #print(SMM2IDA)
                                    SMM2IDB = SMM2ID2Str[4:10]
                                    #print(SMM2IDB)
                                    SMM2IDC = SMM2ID2Str[10:30]
                                    #print(SMM2IDC)
                                    SMM2IDD = SMM2ID2Str[30:31]
                                    #print(SMM2IDD)
                                    SMM2IDE = SMM2ID2Str[31:32]
                                    #print(SMM2IDE)
                                    SMM2IDF = SMM2ID2Str[32:44]
                                    #print(SMM2IDF)
                                    if SMM2IDA == "1000" and SMM2IDE == "1":
                                        #print("True")
                                        SMM2IDGKBH = SMM2IDF + SMM2IDC #00010111110010110101111110011101
                                        #SMM2ID16 = hex(int(SMM2IDGKBH)) 
                                        #SMM2ID16 = ''.join([hex(i) for i in [int(b, 2) for b in SMM2IDGKBH.split(' ')]])
                                        #print(SMM2ID16)
                                        #SMM2ID16Xor = SMM2ID16 ^ hex(0x1680E07C)
                                        for i in [int(b, 2) for b in SMM2IDGKBH.split(' ')]:
                                            SMM2IDXor10 = int(hex(i),16) ^ int(hex(0x1680E07C),16)
                                            #print(SMM2ID16Xor)
                                        #print(SMM2IDXor10)
                                        SMM2ID16Xor = hex(SMM2IDXor10)
                                        #print(SMM2ID16Xor)
                                        for i in [int(b, 2) for b in SMM2IDB.split(' ')]:
                                            SMM2IDB10 = int(i)
                                        #print(SMM2IDB10)
                                        if (SMM2IDXor10 - 31) % 64 == SMM2IDB10:
                                            #print("mod True")
                                            if SMM2IDD == "0":
                                                SMM2IDType = 0
                                                SMM2APIRequest = demjson.decode(SMM2API.level_info(proxyserverip,proxyserverhost,id))
                                                SMM2LevelTagType = SMM2APIRequest.get("tags_name")[0]
                                                if len(SMM2APIRequest.get("tags_name")) > 1:
                                                    for i in SMM2APIRequest.get("tags_name"):
                                                        if SMM2LevelTagType != str(i):
                                                            SMM2LevelTagType += ',' + str(i)
                                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(SMM2APIRequest)})
                                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']\n[CQ:image,file=file:///'+str(SMM2API.level_thumbnail(proxyserverip,proxyserverhost,id))+']\n关卡名称:'+str(SMM2APIRequest.get("name"))+'\n关卡简介:'+str(SMM2APIRequest.get("description"))+'\n上传时间:'+str(SMM2APIRequest.get("uploaded_pretty"))+'\n关卡编号:'+str(SMM2APIRequest.get("data_id"))+'\n关卡游戏类型:'+str(SMM2APIRequest.get("game_style_name"))+'\n关卡默认主题:'+str(SMM2APIRequest.get("theme_name"))+'\n关卡难度:'+str(SMM2APIRequest.get("difficulty_name"))+'\n关卡标签:'+str(SMM2LevelTagType) + '[CQ:image,file=file:///'+str(SMM2API.level_entire_thumbnail(proxyserverip,proxyserverhost,id))+']'})
                                            elif SMM2IDD == "1":
                                                SMM2IDType = 1
                                                SMM2APIRequest = demjson.decode(SMM2API.user_info(proxyserverip,proxyserverhost,id))
                                                #send_msg({'msg_type':str(messagetype),'number':sendid,'msg':str(SMM2APIRequest)})
                                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']\n[CQ:image,file=file:///'+str(SMM2API.proxy_download_img(proxyserverip,proxyserverhost,SMM2APIRequest.get("mii_image")))+']\n玩家名:'+str(SMM2APIRequest.get("name"))+'\n玩家所在国家:'+str(SMM2APIRequest.get("country"))+'\n玩家所在区域:'+str(SMM2APIRequest.get("region_name"))+'\n玩家编号:'+str(SMM2APIRequest.get("pid"))+'\n玩家最后一次上线:'+str(SMM2APIRequest.get("last_active_pretty"))+'\n游玩过的关卡数:'+str(SMM2APIRequest.get("courses_played"))+'\n通关过的关卡数:'+str(SMM2APIRequest.get("courses_cleared"))+'\n尝试过的关卡数:'+str(SMM2APIRequest.get("courses_attempted"))+'\n死亡过的关卡数:'+str(SMM2APIRequest.get("courses_deaths"))+'\n点赞数:'+str(SMM2APIRequest.get("likes"))+'\n创作点数:'+str(SMM2APIRequest.get("maker_points"))+'\n最后一次上传地图:'+str(SMM2APIRequest.get("last_uploaded_level_pretty"))+'\n玩家超级世界ID:'+str(SMM2APIRequest.get("super_world_id"))})
                                            else:
                                                send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']呜XwX!!!ID解密失败(所有效验通过之后类型区竟然不是0和1！)'})
                                                continue
                                        else:
                                            #print("mod False")
                                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']呜XwX!!!ID解密失败(解密后效验区与通过关卡编号计算的不符合)'})
                                            continue
                                    else:
                                        #print("False")
                                        send_msg({'msg_type':str(messagetype),'number':sendid,'msg':"[CQ:at,qq="+str(qq)+']呜XwX!!!ID解密失败(解密后的44位二进制中A和E非定数值)'})
                                        continue
                    elif messagecommand[0:8] == '今天可以玩游戏吗' or messagecommand[0:9] == '今天可以玩游戏吗?' or messagecommand[0:9] == '今天可以玩游戏吗？':
                        fcmstrjson = '{"FCMcalendar_list":'
                        fcmurl = "https://download.jiazhang.qq.com/mouthOptions-"+str(time.strftime("%Y%m",time.localtime()))+".js"
                        print("当月网址："+fcmurl)
                        FCMcalendar_js = requests.get(fcmurl)
                        #print(FCMcalendar_js)
                        fcmstrjson = fcmstrjson + str(str(FCMcalendar_js.text)[str(FCMcalendar_js.text).find("["):str(FCMcalendar_js.text).rfind("]")+1]).replace(" ","").replace("\n","") + "}"
                        FCMcalendar_list = json.loads(fcmstrjson).get("FCMcalendar_list")
                        print("当月和次月游玩日："+str(FCMcalendar_list))
                        if str(FCMcalendar_list[0][int(time.strftime(r"%d",time.localtime()))-1]) == "1":
                            lastday = str(FCMcalendar_list[0][int(time.strftime(r"%d",time.localtime()))-1:len(FCMcalendar_list[0])].index(0))
                            print(f"今天可以游玩一小时！！！不过还有{lastday}天就结束了xwx")
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':f"[CQ:at,qq={qq}] [CQ:face,id=12]今天可以游玩一小时！！！不过还有{lastday}就结束了xwx"})
                        else:
                            lastday = str(FCMcalendar_list[0][int(time.strftime(r"%d",time.localtime()))-1:len(FCMcalendar_list[0])].index(1))
                            print(f"今天不可以XwX，不过再等{lastday}天就可以玩了awa")
                            send_msg({'msg_type':str(messagetype),'number':sendid,'msg':f"[CQ:at,qq={qq}] [CQ:face,id=9]今天不可以XwX，不过再等{lastday}天就可以玩了awa"})
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
                        if menulistline[0:3] == "---":
                            menumessage = menumessage + str("\n")+menulistline
                        elif menulistline[0:1].isdigit() == True:
                            menumessage = menumessage + str("\n")+menulistline
                        else:
                            menumessage = menumessage + str("\n")+'[CQ:face,id=66]'+menulistline
                    menumessage = menumessage + str("\n")+"-------------------"+str("\n")+MintBotVersion
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':menumessage})
                if message == str("[CQ:at,qq="+QQID+"] ") or message == str("[CQ:at,qq="+QQID+"]"):
                    print('收到菜单指令')
                    menumessage = '[CQ:face,id=12]嗷呜，欢迎使用'+BotName+'机器人，这是我可以做的事情OwO：'
                    for menulistline in menulist:
                        if menulistline[0:3] == "---":
                            menumessage = menumessage + str("\n")+menulistline
                        elif menulistline[0:1].isdigit() == True:
                            menumessage = menumessage + str("\n")+menulistline
                        else:
                            menumessage = menumessage + str("\n")+'[CQ:face,id=66]'+menulistline
                    menumessage = menumessage + str("\n")+"-------------------"+str("\n")+MintBotVersion
                    send_msg({'msg_type':str(messagetype),'number':sendid,'msg':menumessage})
                    
        except SystemExit as error:
                   print('解释器请求退出：'+str(error))
                   crashlogsave("总代码(解释器请求退出):"+str(error))
                   continue
        except KeyboardInterrupt as error:
                   print('用户中断执行(通常是输入^C)：'+str(error))
                   crashlogsave("总代码(用户中断执行(通常是输入^C)):"+str(error))
                   continue
        except StopIteration as error:
                   print('迭代器没有更多的值：'+str(error))
                   crashlogsave("总代码(迭代器没有更多的值):"+str(error))
                   continue
        except GeneratorExit as error:
                   print('生成器(generator)发生异常来通知退出：'+str(error))
                   crashlogsave("总代码(生成器(generator)发生异常来通知退出):"+str(error))
                   continue
        except ArithmeticError as error:
                   print('所有数值计算错误的基类：'+str(error))
                   crashlogsave("总代码(所有数值计算错误的基类):"+str(error))
                   continue
        except FloatingPointError as error:
                   print('浮点计算错误：'+str(error))
                   crashlogsave("总代码(浮点计算错误):"+str(error))
                   continue
        except OverflowError as error:
                   print('数值运算超出最大限制：'+str(error))
                   crashlogsave("总代码(数值运算超出最大限制):"+str(error))
                   continue
        except ZeroDivisionError as error:
                   print('除(或取模)零 (所有数据类型)：'+str(error))
                   crashlogsave("总代码(除(或取模)零 (所有数据类型)):"+str(error))
                   continue
        except AssertionError as error:
                   print('断言语句失败：'+str(error))
                   crashlogsave("总代码(断言语句失败):"+str(error))
                   continue
        except AttributeError as error:
                   print('对象没有这个属性：'+str(error))
                   crashlogsave("总代码(对象没有这个属性):"+str(error))
                   continue
        except EOFError as error:
                   print('没有内建输入,到达EOF 标记：'+str(error))
                   crashlogsave("总代码(没有内建输入,到达EOF 标记):"+str(error))
                   continue
        except EnvironmentError as error:
                   print('操作系统错误的基类：'+str(error))
                   crashlogsave("总代码(操作系统错误的基类):"+str(error))
                   continue
        except IOError as error:
                   print('输入/输出操作失败：'+str(error))
                   crashlogsave("总代码(输入/输出操作失败):"+str(error))
                   continue
        except OSError as error:
                   print('操作系统错误：'+str(error))
                   crashlogsave("总代码(操作系统错误):"+str(error))
                   continue
        except WindowsError as error:
                   print('系统调用失败：'+str(error))
                   crashlogsave("总代码(系统调用失败):"+str(error))
                   continue
        except ImportError as error:
                   print('导入模块/对象失败：'+str(error))
                   crashlogsave("总代码(导入模块/对象失败):"+str(error))
                   continue
        except LookupError as error:
                   print('无效数据查询的基类：'+str(error))
                   crashlogsave("总代码(无效数据查询的基类):"+str(error))
                   continue
        except IndexError as error:
                   print('序列中没有此索引(index)：'+str(error))
                   crashlogsave("总代码(序列中没有此索引(index)):"+str(error))
                   continue
        except KeyError as error:
                   print('映射中没有这个键：'+str(error))
                   crashlogsave("总代码(映射中没有这个键):"+str(error))
                   continue
        except MemoryError as error:
                   print('内存溢出错误(对于Python 解释器不是致命的)：'+str(error))
                   crashlogsave("总代码(内存溢出错误(对于Python 解释器不是致命的)):"+str(error))
                   continue
        except NameError as error:
                   print('未声明/初始化对象 (没有属性)：'+str(error))
                   crashlogsave("总代码(未声明/初始化对象 (没有属性)):"+str(error))
                   continue
        except UnboundLocalError as error:
                   print('访问未初始化的本地变量：'+str(error))
                   crashlogsave("总代码(访问未初始化的本地变量):"+str(error))
                   continue
        except ReferenceError as error:
                   print('弱引用(Weak reference)试图访问已经垃圾回收了的对象：'+str(error))
                   crashlogsave("总代码(弱引用(Weak reference)试图访问已经垃圾回收了的对象):"+str(error))
                   continue
        except RuntimeError as error:
                   print('一般的运行时错误：'+str(error))
                   crashlogsave("总代码(一般的运行时错误):"+str(error))
                   continue
        except NotImplementedError as error:
                   print('尚未实现的方法：'+str(error))
                   crashlogsave("总代码(尚未实现的方法):"+str(error))
                   continue
        except SyntaxError as error:
                   print('Python 语法错误：'+str(error))
                   crashlogsave("总代码(Python 语法错误):"+str(error))
                   continue
        except IndentationError as error:
                   print('缩进错误：'+str(error))
                   crashlogsave("总代码(缩进错误):"+str(error))
                   continue
        except TabError as error:
                   print('Tab 和空格混用：'+str(error))
                   crashlogsave("总代码(Tab 和空格混用):"+str(error))
                   continue
        except SystemError as error:
                   print('一般的解释器系统错误：'+str(error))
                   crashlogsave("总代码(一般的解释器系统错误):"+str(error))
                   continue
        except TypeError as error:
                   print('对类型无效的操作：'+str(error))
                   crashlogsave("总代码(对类型无效的操作):"+str(error))
                   continue
        except ValueError as error:
                   print('传入无效的参数：'+str(error))
                   crashlogsave("总代码(传入无效的参数):"+str(error))
                   continue
        except UnicodeError as error:
                   print('Unicode 相关的错误：'+str(error))
                   crashlogsave("总代码(Unicode 相关的错误):"+str(error))
                   continue
        except UnicodeDecodeError as error:
                   print('Unicode 解码时的错误：'+str(error))
                   crashlogsave("总代码(Unicode 解码时的错误):"+str(error))
                   continue
        except UnicodeEncodeError as error:
                   print('Unicode 编码时错误：'+str(error))
                   crashlogsave("总代码(Unicode 编码时错误):"+str(error))
                   continue
        except UnicodeTranslateError as error:
                   print('Unicode 转换时错误：'+str(error))
                   crashlogsave("总代码(Unicode 转换时错误):"+str(error))
                   continue
        except Warning as error:
                   print('警告的基类：'+str(error))
                   crashlogsave("总代码(警告的基类):"+str(error))
                   continue
        except DeprecationWarning as error:
                   print('关于被弃用的特征的警告：'+str(error))
                   crashlogsave("总代码(关于被弃用的特征的警告):"+str(error))
                   continue
        except FutureWarning as error:
                   print('关于构造将来语义会有改变的警告：'+str(error))
                   crashlogsave("总代码(关于构造将来语义会有改变的警告):"+str(error))
                   continue
        except PendingDeprecationWarning as error:
                   print('关于特性将会被废弃的警告：'+str(error))
                   crashlogsave("总代码(关于特性将会被废弃的警告):"+str(error))
                   continue
        except RuntimeWarning as error:
                   print('可疑的运行时行为(runtime behavior)的警告：'+str(error))
                   crashlogsave("总代码(可疑的运行时行为(runtime behavior)的警告):"+str(error))
                   continue
        except SyntaxWarning as error:
                   print('可疑的语法的警告：'+str(error))
                   crashlogsave("总代码(可疑的语法的警告):"+str(error))
                   continue
        except UserWarning as error:
                   print('用户代码生成的警告：'+str(error))
                   crashlogsave("总代码(用户代码生成的警告):"+str(error))
                   continue
        #except OverflowWarning as error:
                   #print('旧的关于自动提升为长整型(long)的警告：'+str(error))
                   #crashlogsave("总代码(旧的关于自动提升为长整型(long)的警告):"+str(error))
                   #continue
        except Exception as error:
                   print('常规错误的基类：'+str(error))
                   crashlogsave("总代码(常规错误的基类):"+str(error))
                   continue
        #except StandardError as error:
                   #print('所有的内建标准异常的基类：'+str(error))
                   #crashlogsave("总代码(所有的内建标准异常的基类):"+str(error))
                   #continue
        except BaseException as error:
                   print('所有异常的基类：'+str(error))
                   crashlogsave("总代码(所有异常的基类):"+str(error))
                   continue
        except:
                   print('未知错误')
                   crashlogsave("总代码(未知错误):"+str(error))
                   continue
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
            #crashlogsave("戳一戳:(Json找不到值)"+str(error))
            #print('Json找不到值：'+str(error))
            continue  
    elif rev["post_type"]=='request':
        #continue
        if rev["request_type"] == 'friend':
            #continue
            if cqhttpaccesstoken == '':
                requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/set_friend_add_request?flag='+rev["flag"] + '&approve=true')
                crashlogsave("添加好友:(QQ号:"+str(rev["user_id"])+")验证信息是:"+str(rev["comment"])+",Flag是:"+str(rev["flag"]))
            else:
                requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/set_friend_add_request?flag='+rev["flag"]+'&approve=true&access_token='+str(cqhttpaccesstoken))
                crashlogsave("添加好友:(QQ号:"+str(rev["user_id"])+")验证信息是:"+str(rev["comment"])+",Flag是:"+str(rev["flag"]))
        elif rev["request_type"] == 'group':
            if rev["sub_type"] == 'invite':
                requests.get('http://'+str(cqhttpserverip)+':'+str(cqhttpserveriphost)+'/set_group_add_request?flag='+rev["flag"]+'&sub_type=invite&approve=true'+'&access_token='+str(cqhttpaccesstoken))
                crashlogsave("邀请进群:(发送请求的QQ号:"+str(rev["user_id"])+")群号是:"+str(rev["group_id"])+"验证信息是:"+str(rev["comment"])+",Flag是:"+str(rev["flag"]))
            else:
                continue
        else:
            continue
    else:
        continue
print('QQ机器人已停止运行')
time.sleep(100)