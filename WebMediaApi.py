import requests
import json
import hashlib
def Sixty03C3():
    sixtysurl = 'https://api.03c3.cn/zb/api.php'
    sixtysrequests = requests.get(sixtysurl).text
    return(sixtysrequests)
def SixtyZhiHu():
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
