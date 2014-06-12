# -*- coding: utf-8 -*-
import urllib
import re
import bs4
import chardet
import codecs

class Spider:
    
    def __init__(self, url):
        self.currentUrl = url
        
    def download_the_page(self):
        rawPage = urllib.urlopen(self.currentUrl).read()
        
        detectResult = chardet.detect(rawPage)
        if detectResult['encoding'] in ['GB2312', 'gb2312', 'EUC-JP']:
            detectResult['encoding'] = 'gb18030'
        rawPage = unicode(rawPage, encoding=detectResult['encoding'])
        
        p = re.compile('<script[\w\W]+?/script>|<script.+?/>|<style[\w\W]+?/style>|<style.+?/>', re.IGNORECASE)
        rawPage = re.sub(p, '', rawPage)    
        
        soupPage = bs4.BeautifulSoup(rawPage)
        return soupPage
    
    def get_link_from_page(self, bsPage, urlOrigin):
        '''
        Get the rawPage from the given url and parse the links from it
        >>> url = "http://www.sina.com.cn"
        >>> newSpider = Spider(url)
        >>> newSpider.get_link_from_page(newSpider.download_the_page(), url)
        http://www.cdedu.com/dasai2/xiaoxue/web/XIAOWEI/MyWeb/JIESHAO/ziwojieshao.htm
        http://www.cdedu.com/dasai2/xiaoxue/web/XIAOWEI/MyWeb/XIAOYUAN/XIAOYUAN.HTM
        http://www.cdedu.com/dasai2/xiaoxue/web/XIAOWEI/MyWeb/diqiuzhimi/ZHUSIYU.HTM
        http://www.cdedu.com/dasai2/xiaoxue/web/XIAOWEI/MyWeb/The%20door%20leaf%20of%20Color/gallery-DISNEY.htm
        http://www.cdedu.com/dasai2/xiaoxue/web/XIAOWEI/MyWeb/Novel/Novel.htm
        
        '''
        urlCollection = []
        urlParent = re.sub(r'/[^/]*?$', '/', urlOrigin)
        urlGrandParent = re.sub(r'/[^/]+?/[^/]*?$', '/', urlOrigin)
        for link in bsPage.find_all('a'):
            linkUrl = unicode(link.get('href'))
            if not re.match(r'^http', linkUrl):
                if re.match(r'^[0-9a-zA-Z].*?\..+?$', linkUrl):
                    linkUrl = urlParent + linkUrl 
                elif re.match(r'^\./.*?\..+?$', linkUrl):
                    linkUrl = urlParent + linkUrl 
                elif re.match(r'^\.\./.*?\..+?$', linkUrl):
                    linkUrl = urlGrandParent + linkUrl
                else: continue 
            urlCollection.append(linkUrl)
        r = codecs.open('result', 'w', 'utf-8')
        for i in range(len(urlCollection)):
            print urlCollection[i]
            r.write(urlCollection[i]+"\n")
        #return urlCollection
    
    def get_text_from_page(self, bsPage):
        return bsPage.get_text("\n", strip = True)
    
    def print_urllist(self, urlCollection):
        for i in range(len(urlCollection)):
            print urlCollection[i]
    
class Controller:
    def __init__(self):
        return
