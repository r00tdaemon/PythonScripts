__author__ = 'Ujjwal'
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

url='http://ask.fm/account/inbox'
cookie=""

userAgent='User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'

headers={'Cookie':cookie,'User-Agent':userAgent}
req=urllib.request.Request(url,headers=headers)
resp=urllib.request.urlopen(req)
respdata=resp.read()
soup=BeautifulSoup(respdata,'html.parser')
soup.encode("utf-8")
next_page='1'

i=0

f=open("convo2.txt","w",encoding='utf-8')
while bool(next_page):

    for tag,dateTag in zip(soup.find_all('h1',{'class':'streamItemContent streamItemContent-question'}),soup.find_all('span',{'class':'streamItemsAge'})):
        try:
            s=str(tag.contents[0].strip()+'\n'+str(tag.contents[1])+'\t'+dateTag['data-hint'].strip()+' '+dateTag.string.strip()+'\n\n')
            f.write(s)
        except IndexError:
            try:
                s=str(tag.contents[0].strip()+'\n'+dateTag['data-hint'].strip()+' '+dateTag.string.strip()+'\n\n')
                f.write(s)
            except KeyError:
                pass
        except KeyError:
            pass
    try:
        next_page=soup.find('a',{'class':"viewMore", 'data-action':"ItemsMore"})['data-url']
        i+=1
        url="http://ask.fm"+next_page
        print(url,"Page",i)
        req=urllib.request.Request(url,headers=headers)
        resp=urllib.request.urlopen(req)
        respdata=resp.read()
        soup=BeautifulSoup(respdata,'html.parser')
        soup.encode("utf-8")
    except TypeError:
        print("no next page found")
        break

f.close()
