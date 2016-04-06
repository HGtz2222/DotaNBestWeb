#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import urllib
import re
from bs4 import BeautifulSoup


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, 'lxml')
    return soup

def getLogo(html):
    pattern = re.compile(r'http://cdn\.dota2\.com/apps/dota2/images/heroes/\S*\.jpg')
    #pattern = re.compile(r'hello')
    match = pattern.findall(html)
    #match = pattern.findall("aaahttp://cdn.dota2.com/apps/dota2/images/heroes/omniknight_vert.jpg")
    return match

def getName(soup):
	rs = soup.body.find_all(style=r'line-height: 32px;font-size: 18px;font-weight: 500;margin-top:10px;')
	return rs[0].contents[0]

def getAttr1(soup):
	rs = soup.body.find_all(id="str")
	return rs[0].string.strip()

def getAttr2(soup):
	rs = soup.body.find_all(id="agi")
	return rs[0].string.strip()

def getAttr3(soup):
	rs = soup.body.find_all(id="int")
	return rs[0].string.strip()

def getAttr4(soup):
	rs = soup.body.find_all(class_="hero-stats")
	return rs

soup = getHtml("http://dotamax.com/hero/detail/omniknight/")

#print getName(soup)
#print getAttr1(soup)
#print getAttr2(soup)
#print getAttr3(soup)
print getAttr4(soup)

