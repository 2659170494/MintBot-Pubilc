import requests
import filetype
import os
#此仓库需要代理才可以正常使用
#本API文档地址:https://tgrcode.com/mm2/docs/
def level_info(proxyip,proxyhost,course_id):
    url = 'https://tgrcode.com/mm2/level_info/'
    request = requests.get(url+str(course_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def user_info(proxyip,proxyhost,maker_id):
    url = 'https://tgrcode.com/mm2/user_info/'
    request = requests.get(url+str(maker_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def level_info_multiple(proxyip,proxyhost,course_id: list):
    url = 'https://tgrcode.com/mm2/level_info_multiple/'
    if len(course_id) > 1:
        ids = str(course_id[0])
        for Listid in course_id:
            if str(Listid) != str(ids):
                ids = ids + ',' + str(Listid)
    else:
        ids = str(course_id[0])
    request = requests.get(url+str(ids),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def level_comments(proxyip,proxyhost,course_id):
    url = 'https://tgrcode.com/mm2/level_comments/'
    request = requests.get(url+str(course_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def level_played(proxyip,proxyhost,course_id):
    url = 'https://tgrcode.com/mm2/level_played/'
    request = requests.get(url+str(course_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def level_deaths(proxyip,proxyhost,course_id):
    url = 'https://tgrcode.com/mm2/level_deaths/'
    request = requests.get(url+str(course_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def level_thumbnail(proxyip,proxyhost,course_id): #这里直接返回本地的图片位置
    url = 'https://tgrcode.com/mm2/level_thumbnail/'
    request = requests.get(url+str(course_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    level_thumbnailfiletype = filetype.guess(request)
    with open(os.getcwd()+r"\smm2tmp."+level_thumbnailfiletype.extension,'wb') as f:
        f.write(request)
    string = str(os.getcwd()+r"\smm2tmp."+level_thumbnailfiletype.extension).strip()
    #string = string.replace("\\","\"")
    return(string)
def level_entire_thumbnail(proxyip,proxyhost,course_id): #这里直接返回本地的图片位置
    url = 'https://tgrcode.com/mm2/level_entire_thumbnail/'
    request = requests.get(url+str(course_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    levelfiletype = filetype.guess(request)
    with open(os.getcwd()+r"\smm2alltmp."+levelfiletype.extension,'wb') as f:
        f.write(request)
    string = str(os.getcwd()+r"\smm2alltmp."+levelfiletype.extension).strip()
    #string = string.replace("\\","\"")
    return(string)
def level_data(proxyip,proxyhost,course_id): #这里直接返回本地的地图文件位置
    url = 'https://tgrcode.com/mm2/level_data/'
    request = requests.get(url+str(course_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    #levelfiletype = filetype.guess(request)
    levelfiletype = "bcd"
    with open(os.getcwd()+r"\smm2LD_"+str(course_id)+"."+levelfiletype,'wb') as f:
        f.write(request)
    string = str(os.getcwd()+r"\smm2LD_"+str(course_id)+"."+levelfiletype).strip()
    #with open(os.getcwd()+r"\smm2LD_"+str(course_id),'wb') as f:
        #f.write(request)
    #string = str(os.getcwd()+r"\smm2LD_"+str(course_id)).strip()
    #string = string.replace("\\","\"")
    return(string)
def level_data_dataid(proxyip,proxyhost,data_id): #这里直接返回本地的地图文件位置
    url = 'https://tgrcode.com/mm2/level_data_dataid/'
    request = requests.get(url+str(data_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    #levelfiletype = filetype.guess(request)
    levelfiletype = "bcd"
    with open(os.getcwd()+r"\smm2LD_"+str(data_id)+"."+levelfiletype,'wb') as f:
        f.write(request)
    string = str(os.getcwd()+r"\smm2LD_"+str(data_id)+"."+levelfiletype).strip()
    #with open(os.getcwd()+r"\smm2LD_"+str(data_id),'wb') as f:
        #f.write(request)
    #string = str(os.getcwd()+r"\smm2LD_"+str(data_id)).strip()
    #string = string.replace("\\","\"")
    return(string)
def ninji_info(proxyip,proxyhost):
    url = 'https://tgrcode.com/mm2/ninji_info/'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def ninji_ghosts(proxyip,proxyhost,index,time,num):
    url = f'https://tgrcode.com/mm2/ninji_ghosts/{index}?&time={time}&num={num}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def ninji_ghosts_time(proxyip,proxyhost,index,time):
    url = f'https://tgrcode.com/mm2/ninji_ghosts/{index}?time={time}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def ninji_ghosts_num(proxyip,proxyhost,index,num):
    url = f'https://tgrcode.com/mm2/ninji_ghosts/{index}?num={num}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def get_posted(proxyip,proxyhost,maker_id):
    url = 'https://tgrcode.com/mm2/get_posted/'
    request = requests.get(url+str(maker_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def get_liked(proxyip,proxyhost,maker_id):
    url = 'https://tgrcode.com/mm2/get_liked/'
    request = requests.get(url+str(maker_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def get_played(proxyip,proxyhost,maker_id):
    url = 'https://tgrcode.com/mm2/get_played/'
    request = requests.get(url+str(maker_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def get_first_cleared(proxyip,proxyhost,maker_id):
    url = 'https://tgrcode.com/mm2/get_first_cleared/'
    request = requests.get(url+str(maker_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def get_world_record(proxyip,proxyhost,maker_id):
    url = 'https://tgrcode.com/mm2/get_first_cleared/'
    request = requests.get(url+str(maker_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def get_super_worlds(proxyip,proxyhost):
    url = 'https://tgrcode.com/mm2/get_super_worlds/'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def super_world(proxyip,proxyhost,super_world_id):
    url = 'https://tgrcode.com/mm2/super_world/'
    request = requests.get(url+str(super_world_id),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_endless_mode(proxyip,proxyhost,count,difficulty):
    url = f'https://tgrcode.com/mm2/search_endless_mode/?count={count}&difficulty={difficulty}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_endless_mode_count(proxyip,proxyhost,count):
    url = f'https://tgrcode.com/mm2/search_endless_mode/?count={count}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_endless_mode_difficulty(proxyip,proxyhost,difficulty):
    url = f'https://tgrcode.com/mm2/search_endless_mode/?difficulty={difficulty}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_new(proxyip,proxyhost):
    url = 'https://tgrcode.com/mm2/search_new/'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_new_count(proxyip,proxyhost,count):
    url = 'https://tgrcode.com/mm2/search_new/?count='
    request = requests.get(url+str(count),proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular(proxyip,proxyhost):
    url = 'https://tgrcode.com/mm2/search_popular/'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_count(proxyip,proxyhost,count):
    url = f'https://tgrcode.com/mm2/search_popular/?count={count}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_count_difficulty(proxyip,proxyhost,count,difficulty):
    url = f'https://tgrcode.com/mm2/search_popular/?count={count}&difficulty={difficulty}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_count_difficulty_rejectRegions(proxyip,proxyhost,count,difficulty,rejectRegions):
    url = f'https://tgrcode.com/mm2/search_popular/?count={count}&difficulty={difficulty}&rejectRegions={rejectRegions}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_count_rejectRegions(proxyip,proxyhost,count,rejectRegions):
    url = f'https://tgrcode.com/mm2/search_popular/?count={count}&rejectRegions={rejectRegions}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_count_rejectRegions_difficulty(proxyip,proxyhost,count,rejectRegions,difficulty):
    url = f'https://tgrcode.com/mm2/search_popular/?count={count}&difficulty={difficulty}&rejectRegions={rejectRegions}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_difficulty(proxyip,proxyhost,difficulty):
    url = f'https://tgrcode.com/mm2/search_popular/?difficulty={difficulty}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_difficulty_count(proxyip,proxyhost,difficulty,count):
    url = f'https://tgrcode.com/mm2/search_popular/?difficulty={difficulty}&count={count}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_difficulty_count_rejectRegions(proxyip,proxyhost,difficulty,count,rejectRegions):
    url = f'https://tgrcode.com/mm2/search_popular/?difficulty={difficulty}&count={count}&rejectRegions={rejectRegions}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_difficulty_rejectRegions(proxyip,proxyhost,difficulty,rejectRegions):
    url = f'https://tgrcode.com/mm2/search_popular/?difficulty={difficulty}&rejectRegions={rejectRegions}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_difficulty_rejectRegions_count(proxyip,proxyhost,difficulty,rejectRegions,count):
    url = f'https://tgrcode.com/mm2/search_popular/?difficulty={difficulty}&rejectRegions={rejectRegions}&count={count}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_rejectRegions(proxyip,proxyhost,rejectRegions):
    url = f'https://tgrcode.com/mm2/search_popular/?rejectRegions={rejectRegions}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_rejectRegions_count(proxyip,proxyhost,rejectRegions,count):
    url = f'https://tgrcode.com/mm2/search_popular/?rejectRegions={rejectRegions}&count={count}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_rejectRegions_count_difficulty(proxyip,proxyhost,rejectRegions,count,difficulty):
    url = f'https://tgrcode.com/mm2/search_popular/?rejectRegions={rejectRegions}&count={count}&difficulty={difficulty}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_rejectRegions_difficulty(proxyip,proxyhost,rejectRegions,difficulty):
    url = f'https://tgrcode.com/mm2/search_popular/?rejectRegions={rejectRegions}&difficulty={difficulty}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def search_popular_rejectRegions_difficulty_count(proxyip,proxyhost,rejectRegions,difficulty,count):
    url = f'https://tgrcode.com/mm2/search_popular/?rejectRegions={rejectRegions}&difficulty={difficulty}&count={count}'
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    return request
def proxy_download_img(proxyip,proxyhost,url): #这里直接返回本地的图片位置
    request = requests.get(url,proxies={'https':'http://'+str(proxyip)+":"+str(proxyhost),"http":'http://'+str(proxyip)+":"+str(proxyhost)}).content
    levelfiletype = filetype.guess(request)
    with open(os.getcwd()+r"\smm2downloadimgtmp."+levelfiletype.extension,'wb') as f:
        f.write(request)
    string = str(os.getcwd()+r"\smm2downloadimgtmp."+levelfiletype.extension).strip()
    #string = string.replace("\\","\"")
    return(string)