import requests
#编创协第三方接口授权:https://bcmcreator.cn/index.php?mod=OAuth#
#编创协接口开放平台:https://api.bcmcreator.cn/
def user_info(id):
    url = 'https://api.bcmcreator.cn/user_base/user_info.php?id=' + str(id)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_info_local(id):
    url = 'http://43.155.60.134:1625/user_base/user_info.php?id=' + str(id)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_matchinfo(id):
    url = 'https://api.bcmcreator.cn/user_base/user_matchinfo.php?id=' + str(id)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_matchinfo_local(id):
    url = 'http://43.155.60.134:1625/user_base/user_matchinfo.php?id=' + str(id)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_matchlogin(oacode,md5,sign,describe):
    url = 'https://api.bcmcreator.cn/user_base/user_matchlogin.php'
    data = {"oacode":oacode,"md5":md5,"sign":sign,"describe":describe}
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def user_matchlogin_local(oacode,md5,sign,describe):
    url = 'http://43.155.60.134:1625/user_base/user_matchlogin.php'
    data = {"oacode":oacode,"md5":md5,"sign":sign,"describe":describe}
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def match_info(t,md5,sign):
    url = 'https://api.bcmcreator.cn/match_base/match_info.php'
    data = {"t":t,"md5":md5,"sign":sign}
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def match_info_local(t,md5,sign):
    url = 'http:/43.155.60.134:1625/match_base/match_info.php'
    data = {"t":t,"md5":md5,"sign":sign}
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def match_enter(t,oacode,md5,sign):
    url = 'https://api.bcmcreator.cn/match_base/match_enter.php'
    data = {"t":t,"oacode":oacode,"md5":md5,"sign":sign}
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def match_enter_local(t,oacode,md5,sign):
    url = 'http://43.155.60.134:1625/match_base/match_enter.php'
    data = {"t":t,"oacode":oacode,"md5":md5,"sign":sign}
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def match_end(t,md5,sign):
    url = 'https://api.bcmcreator.cn/match_base/match_end.php'
    data = {"t":t,"md5":md5,"sign":sign}
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def match_end_local(t,md5,sign):
    url = 'http://43.155.60.134:1625/match_base/match_end.php'
    data = {"t":t,"md5":md5,"sign":sign}
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def user_info_code_Plus(code):
    url = 'https://api.bcmcreator.cn/user_info.php?code=' + str(code)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_info_code_Plus_local(code):
    url = 'http://43.155.60.134:1625/user_info.php?code=' + str(code)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_info_xjm_Plus(xjm):
    url = 'https://api.bcmcreator.cn/user_info.php?xjm=' + str(xjm)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_info_xjm_Plus_local(xjm):
    url = 'http://43.155.60.134:1625/user_info.php?xjm=' + str(xjm)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_destroyCode(code):
    url = "https://api.bcmcreator.cn/user_destroyCode.php?code=" + str(code)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_destroyCode_local(code):
    url = "http://43.155.60.134:1625/user_destroyCode.php?code=" + str(code)
    urlrequests = requests.get(url).text
    return(urlrequests)
def association_log(limit):
    url = 'https://api.bcmcreator.cn/user_base/association_log.php?limit=' + str(limit)
    urlrequests = requests.get(url).text
    return(urlrequests)
def association_log_local(limit):
    url = 'http://43.155.60.134:1625/user_base/association_log.php?limit=' + str(limit)
    urlrequests = requests.get(url).text
    return(urlrequests)
def association_log_uid(uid,limit):
    url = 'https://api.bcmcreator.cn/user_base/association_log.php?limit=' + str(limit) + '&uid=' + str(uid)
    urlrequests = requests.get(url).text
    return(urlrequests)
def association_log_uid_local(uid,limit):
    url = 'http://43.155.60.134:1625/user_base/association_log.php?limit=' + str(limit) + '&uid=' + str(uid)
    urlrequests = requests.get(url).text
    return(urlrequests)
def association_log_id(id,limit):
    url = 'https://api.bcmcreator.cn/user_base/association_log.php?limit=' + str(limit) + '&id=' + str(id)
    urlrequests = requests.get(url).text
    return(urlrequests)
def association_log_id_local(id,limit):
    url = 'http://43.155.60.134:1625/user_base/association_log.php?limit=' + str(limit) + '&id=' + str(id)
    urlrequests = requests.get(url).text
    return(urlrequests)
def association_log_allid(id,uid,limit):
    url = 'https://api.bcmcreator.cn/user_base/association_log.php?limit=' + str(limit) + '&id=' + str(id)
    urlrequests = requests.get(url).text
    return(urlrequests)
def association_log_allid_local(id,uid,limit):
    url = 'http://43.155.60.134:1625/user_base/association_log.php?limit=' + str(limit) + '&id=' + str(id)
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_workdata(BcxOA):
    data = {'code':str(BcxOA)}
    url = 'https://api.bcmcreator.cn/user_base/user_workdata.php'
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def user_workdata_local(BcxOA):
    data = {'code':str(BcxOA)}
    url = 'http://43.155.60.134:1625/user_base/user_workdata.php'
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def user_workdata7():
    url = 'https://api.bcmcreator.cn/user_base/user_workdata7.php'
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_workdata7_local():
    url = 'http://43.155.60.134:1625/user_base/user_workdata7.php'
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_workintroduce(code):
    url = f'https://api.bcmcreator.cn/user_base/user_workintroduce.php?code={code}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_workintroduce_local(code):
    url = f'http://43.155.60.134:1625/user_base/user_workintroduce.php?code={code}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def robot(text,otherparty): #我 控 我 自 己
    url = f'https://api.bcmcreator.cn/robot.php?text={text}&otherparty={otherparty}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def robot_local(text,otherparty):
    url = f'http://43.155.60.134:1625/robot.php?text={text}&otherparty={otherparty}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def user_bcmlogin(user,pwd):
    data = {'user':str(user),'pwd':str(pwd)}
    url = 'https://api.bcmcreator.cn/login/user_bcmlogin.php'
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def user_bcmlogin_local(user,pwd):
    data = {'user':str(user),'pwd':str(pwd)}
    url = 'http://43.155.60.134:1625/login/user_bcmlogin.php'
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def qq_bcmlogin(rd):
    url = f'https://api.bcmcreator.cn/login/qq_bcmlogin.php?rd={rd}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def qq_bcmlogin_local(rd):
    url = f'http://43.155.60.134:1625/login/qq_bcmlogin.php?rd={rd}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def wx_bcmlogin(rd):
    url = f'https://api.bcmcreator.cn/login/wx_bcmlogin.php?rd={rd}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def wx_bcmlogin_local(rd):
    url = f'http://43.155.60.134:1625/login/wx_bcmlogin.php?rd={rd}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def code_bcmlogin(rd,code,parameter):
    url = f'https://api.bcmcreator.cn/login/code_bcmlogin.php?rd={rd}&code={code}&parameter={parameter}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def code_bcmlogin_local(rd,code,parameter):
    url = f'http://43.155.60.134:1625/login/code_bcmlogin.php?rd={rd}&code={code}&parameter={parameter}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def email(sign,md5,title,email,main,type):
    data = {'sign':str(sign),'md5':str(md5),'title':str(title),'email':str(email),'main':str(main),'type':str(type)}
    url = 'https://api.bcmcreator.cn/email.php'
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def email_local(sign,md5,title,email,main,type):
    data = {'sign':str(sign),'md5':str(md5),'title':str(title),'email':str(email),'main':str(main),'type':str(type)}
    url = 'http://43.155.60.134:1625/email.php'
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def match_query(id):
    url = f'https://api.bcmcreator.cn/match_base/match_query.php?id={id}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def match_query_local(id):
    url = f'http://43.155.60.134:1625/match_base/match_query.php?id={id}'
    urlrequests = requests.get(url).text
    return(urlrequests)
def RoomChat(sender_id,room_id,message):
    data = {"sender_id":str(sender_id),"room_id":str(room_id),"message":str(message)}
    url = "https://api.bcmcreator.cn/chat/RoomChat.php"
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def RoomChat_local(sender_id,room_id,message):
    data = {"sender_id":str(sender_id),"room_id":str(room_id),"message":str(message)}
    url = "http://43.155.60.134:1625/chat/RoomChat.php"
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def GetChat(room_id,limit):
    url = f"https://api.bcmcreator.cn/chat/getChat.php?room_id={room_id}&limit={limit}"
    urlrequests = requests.get(url).text
    return(urlrequests)
def GetChat_local(room_id,limit):
    url = f"http://43.155.60.134:1625/chat/getChat.php?room_id={room_id}&limit={limit}"
    urlrequests = requests.get(url).text
    return(urlrequests)
def getChatUser(sender_id):
    url = f"https://api.bcmcreator.cn/chat/getChatUser.php?sender_id={sender_id}"
    urlrequests = requests.get(url).text
    return(urlrequests)
def getChatUser_local(sender_id):
    url = f"http://43.155.60.134:1625/chat/getChatUser.php?sender_id={sender_id}"
    urlrequests = requests.get(url).text
    return(urlrequests)
def getChatUser_user_name(user_name):
    url = f"https://api.bcmcreator.cn/chat/getChatUser.php?user_name={user_name}"
    urlrequests = requests.get(url).text
    return(urlrequests)
def getChatUser_user_name_local(user_name):
    url = f"http://43.155.60.134:1625/chat/getChatUser.php?user_name={user_name}"
    urlrequests = requests.get(url).text
    return(urlrequests)
def RoomChat_meid(sender_id,room_id,message,meid):
    data = {"meid":str(meid),"sender_id":str(sender_id),"room_id":str(room_id),"message":str(message)}
    url = "https://api.bcmcreator.cn/chat/RoomChat.php"
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def RoomChat_meid_local(sender_id,room_id,message,meid):
    data = {"meid":str(meid),"sender_id":str(sender_id),"room_id":str(room_id),"message":str(message)}
    url = "http://43.155.60.134:1625/chat/RoomChat.php"
    urlrequests = requests.post(url,data=data).text
    return(urlrequests)
def getBlog():
    url = "http://api.bcmcreator.cn/user_base/getBlog.php"
    urlrequests = requests.get(url).text
    return(urlrequests)
def getBlog_local():
    url = "http://43.155.60.134:1625/user_base/getBlog.php"
    urlrequests = requests.get(url).text
    return(urlrequests)