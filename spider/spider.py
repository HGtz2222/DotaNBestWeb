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
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getLogo(soup):
	rs = soup.body.find_all(style='width: 50px;height: 50px;padding: 12px;float: left;')
	return rs[0].attrs['src'].strip()

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

# TODO
# 攻击
def getAttr4(soup):
	return 4

# 护甲
def getAttr5(soup):
	return 5

# 移速
def getAttr6(soup):
	#rs = soup.body.find_all(class_="hero-stats")
	#return rs[2].span.string.strip()
	return 6

# DPS
def getAttr7(soup):
	#rs = soup.body.find_all(id="dps")
	#return rs[0].string
	return 7

# 生命 TODO
def getAttr8(soup):
	#rs = soup.body.find_all(id="health")
	#return rs[0].string
	return 8

# 魔法 TODO
def getAttr9(soup):
	#rs = soup.body.find_all(id="mana")
	#return rs[0].string
	return 9

# 转身速度 TODO
def getAttr10(soup):
	#rs = soup.body.find_all(class_="hero-stats")
	#return rs[6].string
	return 10

# 攻击前摇
def getAttr11(soup):
	return 11

def get_skill_cnt(skills):
	# - 1是去掉 "属性附加"
	return len(skills) - 1

def get_item_cnt(items):
	cnt = 0
	for item in items:
		try:
			if item.attrs.get('class')[0] == u'attribVal':
				cnt += 1;
		except Exception, e:
			pass
	return cnt


def getSkills(soup):
	rs = soup.body.find_all(style="font-weight: bold;margin-left: 10px;margin-top:10px;width: 93%;height: 62px; line-height: 42px;font-size: 16px;font-weight: 500;")
	rs2 = soup.body.find_all(style="margin-left:auto;margin-right:auto;padding: 10px;")
	skill_cnt = get_skill_cnt(rs2)
	#print "skill_cnt:" + str(skill_cnt)
	skills = []
	for i in range(0, skill_cnt):
		#print "skill: " + str(i)

		skill_name = rs[i].contents[1].strip()
		skill_logo = rs[i].contents[0].attrs["src"].strip()
		desc1 = rs2[i].contents[0].string.strip()
		desc2 = rs2[i].contents[1].string.strip()
		# 需要先探测下有几个扩展属性. 通过attribVal类的数目来判定.
		item_list = rs2[i].contents
		item_cnt = get_item_cnt(item_list)
		#print "cnt:" + str(item_cnt)
		
		cur = 0
		k_index = 3
		items = []
		while cur < item_cnt:
			k = item_list[k_index]
			v = item_list[k_index + 1].string.strip()
			#print k,v
			items.append({'k':k, 'v':v})
			cur += 1
			k_index += 3

		skill = {
			'name' : skill_name,
			'desc1' : desc1,
			'desc2' : desc2,
			'logo' : skill_logo,
			'item' : items
		}
		skills.append(skill)
	return skills

def get_hero_detail(soup):
	'''
		入口函数, 获取英雄的完整信息
	'''
	hero_detail = {
		'name' : getName(soup),
		'logo' : getLogo(soup),
		'liliang' : getAttr1(soup),
		'minjie' : getAttr2(soup),
		'zhili' : getAttr3(soup),
		'gongji' : getAttr4(soup),
		'hujia' : getAttr5(soup),
		'yidongsudu' : getAttr6(soup),
		'gongjisudu' : getAttr7(soup),
		'hp' : getAttr8(soup),
		'mp' : getAttr9(soup),
		'zhuanshensudu' : getAttr10(soup),
		'gongjiqianyao' : getAttr11(soup),
		'skill' : getSkills(soup)
	}
	return hero_detail



soup = getHtml("http://dotamax.com/hero/detail/omniknight/")

#print getName(soup)
#print getAttr1(soup)
#print getAttr2(soup)
#print getAttr3(soup)
#print getAttr6(soup)
#print getAttr8(soup)
#print getAttr10(soup)
#print getSkills(soup)
#print getLogo(soup)
print get_hero_detail(soup)

