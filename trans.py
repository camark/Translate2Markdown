#/usr/bin/env python
#coding=utf8
 
import httplib
import md5
import urllib
import random
import json

appid = '2015063000000001'
secretKey = '12345678'

def query(q):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        response = httpClient.getresponse()
        result=response.read()
        retjson=json.loads(result)
        if(retjson["trans_result"][0]["dst"] == q):
            return (54006, "Unkown keyword error")
        else:
            return (0, retjson["trans_result"][0]["dst"])
    except Exception, e:
        print result
        if(retjson):
            try:
                errcode = int(retjson['error_code'])
                errmsg = retjson['error_msg']
            except Exception, e:
                errcode=54007
                errmsg="Unkown Error"
            return (errcode, errmsg)
        else:
            return (54008, "Fatal error")
    finally:
        if(httpClient):
            httpClient.close()


print query("apple")[1]
print query("aabbc")[1]