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
	'''
	# 从dotamax获取
	rs = soup.body.find_all(style='width: 50px;height: 50px;padding: 12px;float: left;')
	return rs[0].attrs['src'].strip()
	'''
	rs = soup.body.find_all(class_='hero_b')
	return rs[0].attrs['src']


def getName(soup):
	'''
	rs = soup.body.find_all(style=r'line-height: 32px;font-size: 18px;font-weight: 500;margin-top:10px;')
	return rs[0].contents[0]
	'''
	rs = soup.body.find_all(class_='hero_name')
	return rs[0].contents[1].string.strip()

def getAttr1(soup):
	# rs = soup.body.find_all(id="str")
	# return rs[0].string.strip()
	rs = soup.body.find_all(id='pro1')
	return rs[0].next_sibling.string.strip()

def getAttr2(soup):
	# rs = soup.body.find_all(id="agi")
	# return rs[0].string.strip()
	rs = soup.body.find_all(id='pro2')
	return rs[0].next_sibling.string.strip()

def getAttr3(soup):
	# rs = soup.body.find_all(id="int")
	# return rs[0].string.strip()
	rs = soup.body.find_all(id='pro3')
	return rs[0].next_sibling.string.strip()

# 攻击
def getAttr4(soup):
	rs = soup.body.find_all(id='pro4')
	return rs[0].next_sibling.string.strip()

# 护甲
def getAttr5(soup):
	rs = soup.body.find_all(id='pro5')
	return rs[0].next_sibling.string.strip()

# 移速
def getAttr6(soup):
	rs = soup.body.find_all(id='pro6')
	return rs[0].next_sibling.string.strip()

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

# 转身速度
def getAttr10(soup):
	'''
	rs = soup.body.find_all(class_="hero-stats")
	return rs[6].contents[2].string.strip()
	'''
	return 10

# 攻击前摇
def getAttr11(soup):
	'''
	rs = soup.body.find_all(class_="hero-stats")
	return rs[7].contents[2].string.strip()
	'''
	return 11

# 视野
def getAttr12(soup):
	rs = soup.body.find_all(width="75")
	return rs[0].contents[0].string.strip()

# 攻击距离
def getAttr13(soup):
	rs = soup.body.find_all(text=u'攻击范围：')
	return rs[0].parent.parent.contents[-2].contents[0].string.strip()


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

def getSkills_old(soup):
	'''
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
	'''
	pass

def getSkills(soup):
	skill_names = soup.body.find_all(class_="skill_intro")
	skill_desc2 = soup.body.find_all(class_="skill_bot")
	skill_logos = soup.body.find_all(class_="skill_b")
	skill_xh = soup.body.find_all(class_="icon_xh")
	skill_lq = soup.body.find_all(class_="icon_lq")
	skill_items = soup.body.find_all(class_="skill_ul clearfix")

	skill_cnt = len(skill_names)
	skills = []
	for i in range(0, skill_cnt):
		skill_name = skill_names[i].contents[0].string.strip()
		desc1 = skill_names[i].contents[2].string.strip()
		try:
			desc2 = skill_desc2[i].string.strip()
		except Exception,e:
			desc2 = ""
		logo = skill_logos[i].attrs['src']
		xh = skill_xh[i].string.split("：")[1]
		lq = skill_lq[i].string.split("：")[1]
		#print skill_name, xh, lq
		items = []
		for item in skill_items[i].contents:
			try:
				k = item.contents[0].contents[0].string.strip()
				v = item.contents[1].string.strip()
				#print k, v
				items.append({'k':k, 'v':v})
			except Exception,e:
				pass
		skills.append({
			'name' : skill_name,
			'desc1' : desc1,
			'desc2' : desc2,
			'logo' : logo,
			'xh' : xh,
			'lq' : lq,
			'item' : items
		})
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
		'shiye' : getAttr12(soup),
		'skill' : getSkills(soup),
		'gongjijuli' : getAttr13(soup)
	}
	return hero_detail

def get_all_hero_entry(main_url):
	soup = getHtml(main_url)
	hero_entry = []
	rs = soup.body.find_all(onclick=re.compile(r"DoNav\('/hero/detail/\S*'\)"))
	for item in rs:
		url = "http://dotamax.com" + item.attrs['onclick'][7:-2]
		name = item.attrs['onclick'][20:-2]
		hero_entry.append((name, url))
	return hero_entry

def get_all_hero_entry2(main_url):
	soup = getHtml(main_url)
	hero_entry = []
	rs = soup.body.find_all(class_="heroPickerIconLink")
	for item in rs:
		url = item.attrs['href']
		name = url[28:-1]
		hero_entry.append((name, url))
	return hero_entry

def merge_hero_entry(url1, url2):
	hero_entry1 = get_all_hero_entry(url1)
	hero_entry2 = get_all_hero_entry2(url2)
	result = {}
	for name, url in hero_entry1:
		result[name] = [url]
	for name, url in hero_entry2:
		if name in result:
			result[name].append(url)
	for name in result:
		print name, result[name]

def get_all_hero_detail():
	hero_list = get_all_hero_entry2("http://www.dota2.com.cn/heroes/")
	data = {}
	for name, url in hero_list:
		soup = getHtml(url)
		print name + " start!"
		detail = get_hero_detail(soup)
		data[name] = detail
	return data

def write_all_hero():
	rs = get_all_hero_detail()

	print '{'
	for i in rs:
		print '"' + i + '"' + ":" + str(rs[i]) + ","
	print '}'
	

#soup = getHtml("http://dotamax.com/hero/detail/omniknight/")
#soup = getHtml("http://db.dota2.com.cn/hero/omniknight/")

#print getName(soup)
#print getAttr1(soup)
#print getAttr2(soup)
#print getAttr3(soup)
#print getAttr4(soup_buf)
#print getAttr6(soup2)
#print getAttr8(soup)
#print getAttr10(soup)
#print getAttr11(soup)
#print getAttr12(soup_buf)
#print getAttr13(soup)
#print getSkills(soup)
#print getLogo(soup)
#print get_hero_detail(soup, soup2)

#print get_all_hero_entry("http://dotamax.com/hero/rate/")
#print get_all_hero_entry2("http://www.dota2.com.cn/heroes/")
#merge_hero_entry("http://dotamax.com/hero/rate/", "http://www.dota2.com.cn/heroes/")
write_all_hero()
