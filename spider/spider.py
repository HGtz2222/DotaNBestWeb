#coding=utf-8
import urllib
import re
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getLogo(html):
    pattern = re.compile(r'http://cdn\.dota2\.com/apps/dota2/images/heroes/\S*\.jpg')
    #pattern = re.compile(r'hello')
    match = pattern.findall(html)
    #match = pattern.findall("aaahttp://cdn.dota2.com/apps/dota2/images/heroes/omniknight_vert.jpg")
    return match

def getName(html):
	pass

html = getHtml("http://dotamax.com/hero/detail/omniknight/")

logo = getLogo(html)
print logo