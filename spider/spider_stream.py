#coding:utf-8
'''
	负责从stream上抓取比赛信息
'''
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import urllib
import time
import json
import datacenter
from log import log_n, log_e, log_d

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def makeTime(time_str):
	return int(time.mktime(time.strptime(time_str,'%Y-%m-%d %H:%M:%S')))

def getMatchList():
	time_beg = makeTime('2016-04-20 00:00:00')
	time_end = makeTime('2016-04-21 00:00:00')
	url = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1?key=93F83F0DA3114AEB77CAC4E353785CA2&language=zh&min_players=10&matches_requested=500&game_mode=1&hero_id=70'
	html = getHtml(url + '&date_min=' + str(time_beg) + '&date_max=' + str(time_end))
	result = eval(html)
	matches = []
	if 'result' in result:
		tmp = result['result']
		if tmp['status'] == 1:
			matches = tmp['matches']
		else:
			log_e('stream Error 1')
	else:
		log_e('stream Error 2')
	return [ match['match_id'] for match in matches ]

def is_winner(slot, radiant_win):
	log_d(str(slot) + str(radiant_win))
	# TODO 这里不对, 跑出来的结果永远都是胜利呢. 需要再仔细看看. steam敢不敢稳定点. 
	player_radiant = True
	if slot & (1 << 8) == 1:
		player_radiant = False
	return radiant_win == player_radiant

def getMatchDetail(match_id):
	url = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1?key=93F83F0DA3114AEB77CAC4E353785CA2&language=zh&match_id=' + str(match_id)
	html = getHtml(url)
	#log_d(html)
	html_rs = json.loads(html)
	result = {}
	players = []
	try:
		result = html_rs['result']
		#log_d(repr(result))
		# 解析每一个英雄的数据
		players = result['players']
	except Exception,e:
		log_e("match detail error " + str(match_id))
		return []
	hero_list = []
	for hero in players:
		hero_detail = {}
		hero_detail['id'] = hero['hero_id']
		hero_detail['win'] = is_winner(hero['player_slot'], result['radiant_win'])
		# TODO 后续会加入到更多的英雄信息
		hero_list.append(hero_detail)
	return hero_list

def getAllMatchDetail(match_list):
	for match_id in match_list:
		hero_list = getMatchDetail(match_id)
		if len(hero_list) == 0:
			hero_list = getMatchDetail(match_id) # 一次失败了, 再重试一次
		datacenter.update_heros(hero_list)

def run():
	'''
		需要做到:
		按时间来抓取一批比赛id, 遍历这一批比赛id的数据, 然后插入到数据库中.
	'''
	start = time.time()
	log_n('start: ')
	datacenter.load()

	match_list = getMatchList()
	getAllMatchDetail(match_list)
	
	datacenter.save()
	log_n('finish: ' + str(time.time() - start))

def test():
	start = time.time()
	log_n('start: ')
	datacenter.load()
	
	########## 测试代码写在这下面 ##########

	hero_list = getMatchDetail('2365934194')
	datacenter.update_heros(hero_list)

	########## 测试代码写在这上面 ##########

	datacenter.save()
	log_n('finish: ' + str(time.time() - start))

#run()
test()