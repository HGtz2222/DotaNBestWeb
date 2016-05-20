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
			print 'stream Error 1'
	else:
		print 'stream Error 2'
	return [ match['match_id'] for match in matches ]

def is_winner(slot, radiant_win):
	player_radiant = True
	if slot & (1 << 8) == 1:
		player_radiant = False
	return radiant_win == player_radiant

def getMatchDetail(match_id):
	url = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1?key=93F83F0DA3114AEB77CAC4E353785CA2&language=zh&match_id=' + str(match_id)
	html = getHtml(url)
	#print html
	html_rs = json.loads(html)
	result = {}
	try:
		result = html_rs['result']
	except Exception,e:
		print "match detail error" + str(match_id)
	#print repr(result)
	# 解析每一个英雄的数据
	players = result['players']
	hero_list = []
	for hero in players:
		hero_detail = {}
		hero_detail['id'] = hero['hero_id']
		hero_detail['win'] = is_winner(hero['player_slot'], result['radiant_win'])
		# TODO 后续会加入到更多的英雄信息
		hero_list.append(hero_detail)
	return hero_list


def getAllMatchDetail(match_list):
	#return [ getMatchDetail(match_id) for match_id in match_list ]


def run():
	'''
		需要做到:
		按时间来抓取一批比赛id, 遍历这一批比赛id的数据, 然后插入到数据库中.
	'''
	print 'start: ' + str(time.time())
	match_list = getMatchList()
	getAllMatchDetail(match_list)
	print 'finish: ' + str(time.time())

def test():
	pass

#run()
test()