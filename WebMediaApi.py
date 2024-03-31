import requests
import json
import hashlib
import urllib.parse
def Sixty03C3(type = "img"):
    #图片：img，文字：text，json图片地址：jsonImg，json文字：jsonText。默认为img
    #文字类型采摘自知乎，但原知乎已经停更。请使用图片功能
    sixtysurl = 'https://api.03c3.cn/api/zb'
    sixtysrequests = requests.get(sixtysurl).text
    return(sixtysrequests)
def SixtyZhiHu():
    #知乎的60s已经停更，推荐使用其它接口或知乎博主
    sixtysurl = 'https://www.zhihu.com/api/v4/columns/c_1261258401923026944/items'
    sixtysrequests = requests.get(sixtysurl).text
    return(sixtysrequests)
def OneDayOneWenV1Today():
    ODOW='https://interface.meiriyiwen.com/article/today?dev=1'
    ODOWrequests = requests.get(ODOW).text
    return(ODOWrequests)
def OneDayOneWenV1FindDay(time):
    ODOW='https://interface.meiriyiwen.com/article/day?dev=1&date='
    ODOWrequests = requests.get(ODOW+str(time)).text
    return(ODOWrequests)
def OneDayOneWenV1Random():
    ODOW='https://interface.meiriyiwen.com/article/random?dev=1'
    ODOWrequests = requests.get(ODOW).text
    return(ODOWrequests)
def BingTodayImg():
    BTI='https://api.mfstudio.cc/bing/index.php'
    BTIWrequests = requests.get(BTI).content
    return(BTIWrequests)
def QweatherV2FindCity(key,name):
    searchweatherurl = "https://geoapi.qweather.com/v2/city/lookup?key="+str(key)+'&location='
    searchweatherrequests = requests.get(searchweatherurl+str(name)).text
    return(searchweatherrequests)
def QweatherV7Today(key,id):
    weatherurl = "https://devapi.qweather.com/v7/weather/now?key="+str(key)+"&location="
    weatherrequests = requests.get(weatherurl+str(id)).text
    return(weatherrequests)
def ZlibV1OK(ZlibraryURL):
    Zlibheader = {'Host':str(ZlibraryURL),'source':'android','accept-encoding':'gzip','user-agent':'okhttp/3.12.13'}
    Zlibrequests = requests.get('https://'+str(ZlibraryURL)+'/eapi/info/ok',headers=Zlibheader).text
    return(Zlibrequests)
def ZlibV1Login(ZlibraryURL,ZlibUserEmail,ZlibPassword):
    Zlibheader = {'Host':str(ZlibraryURL),'source':'android','accept-encoding':'gzip','user-agent':'okhttp/3.12.13'}
    Zlibloginurl = 'https://'+str(ZlibraryURL)+'/eapi/user/login'
    Zliblogindata = {'email':ZlibUserEmail,'password':ZlibPassword}
    Zlibloginrequests = requests.post(Zlibloginurl,data=Zliblogindata,headers=Zlibheader)
    Zliblogindict = {"data":Zlibloginrequests.text,"cookies":Zlibloginrequests.cookies}
    return(json.dumps(Zliblogindict))
def ZlibV1FindBookName(ZlibraryURL,name):
    Zlibheader = {'Host':str(ZlibraryURL),'source':'android','accept-encoding':'gzip','user-agent':'okhttp/3.12.13'}
    booknamehex = str(name).encode('utf-8').hex()
    booksearchurl = 'https://'+str(ZlibraryURL)+'/eapi/book/search'
    booksearchdata = {"message":str(booknamehex),"languages"+"[]":"","extensions"+"[]":"","order":"popular"}
    booksearchrequests = requests.post(booksearchurl,data=json.dumps(booksearchdata),headers=Zlibheader).text
    return(booksearchrequests)
def MoYuDayVVHan(types = None):
    MoYuUrl = "https://api.vvhan.com/api/moyu"
    if types != None:
        MoYuUrl += f'?type={types}'
    MoYuJsonGet = requests.get(MoYuUrl).content
    return MoYuJsonGet
def MoYuDayJ4U():
    MoYuUrl = "https://api.j4u.ink/v1/store/other/proxy/remote/moyu.json"
    MoYuJsonGet = requests.get(MoYuUrl).text
    return MoYuJsonGet
def MoYuDayQQSUU(types = None):
    #types=json 以json返回地址，默认图片
    MoYuUrl = "https://dayu.qqsuu.cn/moyuribao/apis.php"
    if types != None:
        MoYuUrl += "?type="+types
    MoYuJsonGet = requests.get(MoYuUrl).content
    return MoYuJsonGet
def MoYuTimeQQSUU(types = None):
    #types=json 以json返回地址，默认图片
    MoYuUrl = "https://dayu.qqsuu.cn/moyurili/apis.php"
    if types != None:
        MoYuUrl += "?type="+types
    MoYuJsonGet = requests.get(MoYuUrl).content
    return MoYuJsonGet
def MoMoAA1(types="json",string):
    #types=text 以纯文本返回地址，types=json 以json返回地址和状态
    #string如为纯数字，则以qq传参。反之以url
    if string.isnumeric():
        momourl = f"https://api.52vmy.cn/api/avath/rua?qq={string}&type={types}"
    else:
        momourl = f"https://api.52vmy.cn/api/avath/rua?url={string}&type={types}"
    respone = requests.get(momourl).text
    return respone
def MoMoWerPlus(string):
    MoApiul = 'https://api.wer.plus/api/ruad?url='+ str(urllib.parse.quote(string))
    #MoApiul = 'http://api.wer.plus:8080/api/ruad?url=' + str(urllib.parse.quote(MoQQimagegetJson.get('imgurl'))) + '&token=' + str(onemingKey)
    #MoApiul = 'http://101.35.149.229:8080/api/ruad?url=' + str(urllib.parse.quote(MoQQimagegetJson.get('imgurl'))) + '&token=' + str(onemingKey)
    Mofilejsonget = requests.get(MoApiul).text
    return Mofilejsonget
def QQHeaderImgBTSTU(qq):
    MoApiQQimageUrl = 'http://api.btstu.cn/qqxt/api.php?qq='+str(qq)
    MoApiQQimageRespone = requests.get(MoApiQQimageUrl).text
    return MoApiQQimageRespone
def MD5_32(text="",type="lower"):
    """
    text：加密文本
    type: 加密类型，默认小写
    """
    res = hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()
    if type.__eq__("lower"):
        return res
    else:
        return res.upper()   
