import requests
import urllib
import hashlib
import os
import filetype
import json
def tuyaV1find_name(name):
    findfriendurl = 'https://duo-api.turka.cn/tuyafriends/?name='
    findfriendrequests = requests.get(findfriendurl+urllib.parse.quote(name)).text
    return(findfriendrequests)
#是的就这么Get一下地址返回值就完事了(雾
def tuyaV1find_id(id):
    findfriendurl = 'https://duo-api.turka.cn/tuyafriends/?id='
    findfriendrequests = requests.get(findfriendurl+urllib.parse.quote(id)).text
    return(findfriendrequests)
def tuyaV1img_id(id):
    findimgurl = 'https://duo-api.turka.cn/tuyafriends/img/'+str(id)+'.png'
    findimgrequests = requests.get(findimgurl).content
    return(findimgrequests)
def tuyaV2find_name(name):
    findfriendurl = 'https://duo-api-v2.turka.cn/tuyafriends/'
    findfriendrequests = requests.get(findfriendurl+urllib.parse.quote(name)).text
    return(findfriendrequests)
def tuyaV2find_img(name):
    findfriendurl = 'https://duo-api-v2.turka.cn/tuyafriends/'
    findfriendrequests = requests.get(findfriendurl+urllib.parse.quote(name)+'/img').content
    findfriendfiletype = filetype.guess(findfriendrequests)
    with open(os.getcwd()+r"\findfriendtmp."+findfriendfiletype.extension,'wb') as f:
        f.write(findfriendrequests)
    string = str(os.getcwd()+r"\findfriendtmp."+findfriendfiletype.extension).strip()
    #string = string.replace('\\',"\"")
    return(string)
def tuyaV3token(appid,appkey):
    tokenurl = "https://qiduo-api.turka.cn/auth/token"
    tokendata = {"appid":appid,"appkey":appkey}
    #tokenheader = {"content-type":"application/json"}
    #tokenrequests = requests.post(tokenurl,data=tokendata,headers=tokenheader)
    tokenrequests = requests.post(tokenurl,data=tokendata)
    #print(tokenrequests.text)
    tokenjson = json.loads(tokenrequests.text)
    #if os.path.exists(os.getcwd()+r'/tuyatokentemp.txt')==True:
        #tokentemp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
    #else:
        #tokentemp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='w+')
    tokentemp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='w+')
    if str(tokenjson.get("status")) == "200":
        print("TuyaToken:"+str(tokenjson.get("data").get("token")))
    else:
        print("TuyaToken(ERROR):"+str(tokenrequests.content))
    tokentemp.write(tokenrequests.text)
    tokentemp.close()
    return tokenrequests.text
def tuyaV3find_name(appid,appkey,name):
    findover = 0
    findfriendurl = "https://qiduo-api.turka.cn/tuyafriends/"+str(name)
    #findfriendurl = "http://210f07c0.nat123.fun:53138/tuyafriends/"+str(name)
    while 3:
        if os.path.exists(os.getcwd()+r'/tuyatokentemp.txt')==True:
            tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
            tuyatoken = tuyatokentmp.read()
            #print(tuyatoken)
            tuyatokenjson = json.loads(tuyatoken)
            #print(tuyatokenjson)
            #print(type(tuyatokenjson))
            if tuyatokenjson.get("status") != 200:
                tuyatokentmp.close()
                tuyaV3token(appid,appkey)
            else:
                tuyatokentmp.close()
                findover = 1
                break
        else:
            tuyaV3token(appid,appkey)
    try:
        tuyatokentmp.close()
    except:
        pass
    tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
    tuyatoken = tuyatokentmp.read()
    #print(tuyatoken)
    tuyatokenjson = json.loads(tuyatoken)
    if str(tuyatokenjson.get("status")) != "200" or findover != 1:
        tuyatokentmp.close()
        return json.dumps({"status":500,"tokenjson":tuyatokenjson,"apijson":""})
    tuyatokentmp.close()
    while 3:
        tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
        tuyatoken = tuyatokentmp.read()
        tuyatokenjson = json.loads(tuyatoken)
        tuyatokenheader = {"Auth": "Bearer "+str(tuyatokenjson.get("data").get("token"))}
        findfriendrequests = requests.get(findfriendurl,headers=tuyatokenheader)
        #print(findfriendrequests.content)
        findfriendjson = json.loads(findfriendrequests.content)
        if str(findfriendjson.get("code")) == "1009":
            tuyatokentmp.close()
            tuyaV3token(appid,appkey)
        else:
            findover = 2
            break
    if str(findfriendjson.get("code")) == "1009" or findover != 2:
        tuyatokentmp.close()
        return json.dumps({"status":501,"tokenjson":tuyatokenjson,"apijson":str(findfriendrequests.text)})
    tuyatokentmp.close()
    return findfriendrequests.content
def tuyaV3find_img_old(appid,appkey,name):
    findover = 0
    findfriendurl = "https://qiduo-api.turka.cn/tuyafriends/"+str(name)+"/img"
    while 3:
        if os.path.exists(os.getcwd()+r'/tuyatokentemp.txt')==True:
            tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
            tuyatoken = tuyatokentmp.read()
            #print(tuyatoken)
            tuyatokenjson = json.loads(tuyatoken)
            if str(tuyatokenjson.get("status")) != "200":
                tuyatokentmp.close()
                tuyaV3token(appid,appkey)
            else:
                tuyatokentmp.close()
                findover = 1
                break
        else:
            tuyaV3token(appid,appkey)
    try:
        tuyatokentmp.close
    except:
        pass
    tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
    tuyatoken = tuyatokentmp.read()
    #print(tuyatoken)
    tuyatokenjson = json.loads(tuyatoken)
    if str(tuyatokenjson.get("status")) != "200" or findover != 1:
        tuyatokentmp.close()
        return json.dumps({"status":500,"tokenjson":tuyatokenjson,"apijson":""})
    tuyatokentmp.close()
    while 3:
        tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
        tuyatoken = tuyatokentmp.read()
        tuyatokenjson = json.loads(tuyatoken)
        tuyatokenheader = {"Auth": "Bearer "+str(tuyatokenjson.get("data").get("token"))}
        findfriendrequests = requests.get(findfriendurl,headers=tuyatokenheader)
        #print(findfriendrequests.content)
        try:
            findfriendjson = json.loads(findfriendrequests.content)
            if str(findfriendjson.get("code")) == "1009":
                tuyatokentmp.close()
                tuyaV3token(appid,appkey)
            else:
                break
        except:
            findover = 2
            break
    if findover != 2:
        tuyatokentmp.close()
        return json.dumps({"status":501,"tokenjson":tuyatokenjson,"apijson":str(findfriendrequests.text)})
    tuyatokentmp.close()
    findfriendfiletype = filetype.guess(findfriendrequests.content)
    with open(os.getcwd()+r"\findfriendtmp."+findfriendfiletype.extension,'wb') as f:
        f.write(findfriendrequests.content)
    string = str(os.getcwd()+r"\findfriendtmp."+findfriendfiletype.extension).strip()
    #string = string.replace('\\',"\"")
    return(string)
def tuyaV3find_img_new(appid,appkey,name,json_enabled):
    findover = 0
    if str(json_enabled).isdigit() == True:
        json_enabled = int(json_enabled)
    else:
        return json.dumps({"status":502,"tokenjson":"","apijson":""})
    findfriendurl = "https://qiduo-api.turka.cn/tuyafriends/"+str(name)+"/img"
    #findfriendurl = "http://210f07c0.nat123.fun:53138/tuyafriends/"+str(name)+"/img"
    while 3:
        if os.path.exists(os.getcwd()+r'/tuyatokentemp.txt')==True:
            tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
            tuyatoken = tuyatokentmp.read()
            #print(tuyatoken)
            tuyatokenjson = json.loads(tuyatoken)
            if str(tuyatokenjson.get("status")) != "200":
                tuyatokentmp.close()
                tuyaV3token(appid,appkey)
            else:
                tuyatokentmp.close()
                findover = 1
                break
        else:
            tuyaV3token(appid,appkey)
    try:
        tuyatokentmp.close
    except:
        pass
    tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
    tuyatoken = tuyatokentmp.read()
    #print(tuyatoken)
    tuyatokenjson = json.loads(tuyatoken)
    if str(tuyatokenjson.get("status")) != "200" or findover != 1:
        tuyatokentmp.close()
        return json.dumps({"status":500,"tokenjson":tuyatokenjson,"apijson":""})
    tuyatokentmp.close()
    """
    while 3:
        tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
        tuyatoken = tuyatokentmp.read()
        tuyatokenjson = json.loads(tuyatoken)
        tuyatokenheader = {"Auth": "Bearer "+str(tuyatokenjson.get("data").get("token"))}
        findfriendrequests = requests.get(findfriendurl,headers=tuyatokenheader)
        #print(findfriendrequests.content)
        try:
            findfriendjson = json.loads(findfriendrequests.content)
            if str(findfriendjson.get("code")) == "1009":
                tuyatokentmp.close()
                tuyaV3token(appid,appkey)
            else:
                break
        except:
            findover = 2
            break
    """
    tuyatokentmp = open(os.getcwd()+r'/tuyatokentemp.txt', mode='r+')
    tuyatoken = tuyatokentmp.read()
    tuyatokenjson = json.loads(tuyatoken)
    tuyatokenheader = {"Auth": "Bearer "+str(tuyatokenjson.get("data").get("token"))}
    findfriendrequests = requests.get(findfriendurl,headers=tuyatokenheader)
    findfriendjson = json.loads(findfriendrequests.content)
    if str(findfriendjson.get("code")) == "0":
        if json_enabled == 0:
            tuyatokentmp.close()
            findfriendrequests = requests.get(findfriendjson.get("data").get("img"),headers=tuyatokenheader)
            print(findfriendjson.get("data").get("img"))
            #print(findfriendrequests.content)
            findfriendfiletype = filetype.guess(findfriendrequests.content)
            #print(findfriendfiletype)
            #print(findfriendfiletype.extension)
            with open(os.getcwd()+r"\findfriendtmp."+findfriendfiletype.extension,'wb') as f:
                f.write(findfriendrequests.content)
            string = str(os.getcwd()+r"\findfriendtmp."+findfriendfiletype.extension).strip()
            #string = string.replace('\\',"\"")
            return(string)
        else:
            return(findfriendrequests.content)
    else:
        return json.dumps({"status":501,"tokenjson":tuyatokenjson,"apijson":str(findfriendrequests.text)})
    #if findover != 2:
        #tuyatokentmp.close()
        #return json.dumps({"status":501,"tokenjson":tuyatokenjson,"apierror":str(findfriendrequests.text)})
def microtailV1random():
    microtailurl = 'https://api.tail.icu/'
    microtailurl = microtailurl+'api/v1/getFursuit/json'
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV1find_id(id):
    microtailurl = 'https://api.tail.icu/'
    microtailurl = microtailurl+'api/v1/getFursuitID/json?fid='+str(id)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV1random_img():
    microtailurl = 'https://api.tail.icu/'
    microtailurl = microtailurl+'api/v1/getFursuit/json'
    microtailrequests = requests.get(microtailurl).content
    microtailjson = json.loads(microtailrequests)
    microtailimg = requests.get(microtailjson.get('data').get("url"))
    microtailfiletype = filetype.guess(microtailimg.content)
    with open(os.getcwd()+r"\microtailtmp."+microtailfiletype.extension,'wb') as f:
        f.write(microtailimg.content)
    string = str(os.getcwd()+r"\microtailtmp."+microtailfiletype.extension).strip()
    #string = string.replace('\\',"\"")
    return(string)
def microtailV1find_id_get_img(id):
    microtailurl = 'https://api.tail.icu/'
    microtailurl = microtailurl+'api/v1/getFursuitID/json?fid='+str(id)
    microtailrequests = requests.get(microtailurl).content
    microtailjson = json.loads(microtailrequests)
    microtailimg = requests.get(microtailjson.get('data').get("url"))
    microtailfiletype = filetype.guess(microtailimg.content)
    with open(os.getcwd()+r"\microtailtmp."+microtailfiletype.extension,'wb') as f:
        f.write(microtailimg.content)
    string = str(os.getcwd()+r"\microtailtmp."+microtailfiletype.extension).strip()
    #string = string.replace("\\","\"")
    return(string)
def microtailV2random(qq,timestamp,authKey):
    apipath = 'api/v2/getFursuitRand'
    microtailurl = 'https://api.tail.icu/'+str(apipath)+'/?qq='+str(qq)+'&sign='+str(microtailV2signstring(apipath,timestamp,authKey)) + '&timestamp=' +str(timestamp)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV2find_id(qq,timestamp,authKey,id):
    apipath = 'api/v2/getFursuitByID'
    microtailurl = 'https://api.tail.icu/'+str(apipath)+'/?fid='+str(id)+'&qq='+str(qq)+'&sign='+str(microtailV2signstring(apipath,timestamp,authKey)) + '&timestamp=' +str(timestamp)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV2find_name(qq,timestamp,authKey,name):
    apipath = 'api/v2/getFursuitByName'
    microtailurl = 'https://api.tail.icu/'+str(apipath)+'/?name='+str(urllib.parse.quote(name))+'&qq='+str(qq)+'&sign='+str(microtailV2signstring(apipath,timestamp,authKey)) + '&timestamp=' +str(timestamp)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV2fid(qq,timestamp,authKey,name):
    apipath = 'api/v2/getFursuitFid'
    microtailurl = 'https://api.tail.icu/'+str(apipath)+'/?name='+urllib.parse.quote(name)+'&qq='+str(qq)+'&sign='+str(microtailV2signstring(apipath,timestamp,authKey)) + '&timestamp=' +str(timestamp)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV2fid_max(qq,timestamp,authKey,name):
    apipath = 'api/v2/getFursuitMaxID'
    microtailurl = 'https://api.tail.icu/'+str(apipath)+'/?name='+urllib.parse.quote(name)+'&qq='+str(qq)+'&sign='+str(microtailV2signstring(apipath,timestamp,authKey)) + '&timestamp=' +str(timestamp)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV2dayfur_random(qq,timestamp,authKey):
    apipath = 'api/v2/DailyFursuit/Rand'
    microtailurl = 'https://api.tail.icu/'+str(apipath)+'/?qq='+str(qq)+'&sign='+str(microtailV2signstring(apipath,timestamp,authKey)) + '&timestamp=' +str(timestamp)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV2dayfur_find_name(qq,timestamp,authKey,name):
    apipath = 'api/v2/DailyFursuit/name'
    microtailurl = 'https://api.tail.icu/'+str(apipath)+'/?name='+urllib.parse.quote(name)+'&qq='+str(qq)+'&sign='+str(microtailV2signstring(apipath,timestamp,authKey)) + '&timestamp=' +str(timestamp)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV2dayfur_find_id(qq,timestamp,authKey,id):
    apipath = 'api/v2/DailyFursuit/id'
    microtailurl = 'https://api.tail.icu/'+str(apipath)+'/?fid='+str(id)+'&qq='+str(qq)+'&sign='+str(microtailV2signstring(apipath,timestamp,authKey)) + '&timestamp=' +str(timestamp)
    microtailrequests = requests.get(microtailurl).text
    return(microtailrequests)
def microtailV2signstring(apiPath,timestamp,authKey): #没写完(或者写寄了(2022.07.23:彳亍了，可以用了))
#def microtailV2signstring(apiPath,authKey): 
    #timestamp = int(time.time())
    #furoriginal = int(str(apiPath)+'-'+str(timestamp)+'-'+str(authKey))
    furoriginal = str(apiPath)+'-'+str(timestamp)+'-'+str(authKey)
    print(furoriginal)
    smallstring = hashlib.md5(furoriginal.encode(encoding='UTF-8')).hexdigest()
    print(smallstring)
    #furhash = int(hashlib.md5())
    #print(furhash)
    ''' #是的，这一大堆完全用不到。。。。
    #furoriginal = bytearray(furoriginal)
    #furhash.update(furoriginal.encode("utf-8"))
    #base64data=base64.b64encode(furhash.digest()).decode('utf-8')
    #funbyte = int(bytes("".join(map(str,furhash.digest(bytearray(furoriginal))))), base=16)
    #funbytearray = bytearray(furoriginal, 'utf-8')
    #print(funbytearray)
    #furhash.update(funbytearray)
    #funhashdigest = furhash.digest()
    #print(funhashdigest)
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
    '''
    return smallstring
def furruiV2random_somebody(imgname,imgtype):
    furruiurl = 'https://cloud.foxtail.cn/api/function/random?name='
    if str(imgtype) == "":
        furruirequests = requests.get(furruiurl+str(imgname)).text
    else:
        furruirequests = requests.get(furruiurl+str(imgname)+'&type='+str(imgtype)).text
    return(furruirequests)
    #Type类型 0.设定 1.毛图 2.插画 留空则全局
def furruiV2random():
    furruiurl = 'https://cloud.foxtail.cn/api/function/random'
    furruirequests = requests.get(furruiurl).text
    return(furruirequests)
def furruiV2get_img(imgid):
    furruiurl = 'https://cloud.foxtail.cn/api/function/pictures?picture=' + str(imgid)
    furruirequests = requests.get(furruiurl).text
    furruiurl = json.loads(furruirequests).get("url")
    '''
    furruiurl = 'https://cloud.foxtail.cn/api/function/obtain?mark='+json.loads(furruirequests).get("mark")
    '''
    furruiimg = requests.get(furruiurl).content
    furruifiletype = filetype.guess(furruiimg)
    with open(os.getcwd()+r"/furruitmp."+furruifiletype.extension,'wb') as f:
        f.write(furruiimg)
    string = str(os.getcwd()+r"/furruitmp."+furruifiletype.extension).strip()
    #string = string.replace("\\","/")
    return(string)
def hifurryV1today():
    todayimgurl = 'https://api.hifurry.cn/everyfur/today.json'
    todayimgrequests = requests.get(todayimgurl).text
    return(todayimgrequests)
def hifurryV1find_day(time):
    todayimgurl = 'https://api.hifurry.cn/everyfur/'+str(time)+'.json'
    todayimgrequests = requests.get(todayimgurl).text
    return(todayimgrequests)

