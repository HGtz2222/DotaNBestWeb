#coding:utf-8
import string
from log import log_n, log_e, log_d

datapath = 'hero_data'

hero_data = {}

def _process(toks):
	'''
		数据结构构造如下: 
		hero_data是一个总的hash表. 
		key为hero_id, value是hero_detail
		hero_detail又是一个hash表, 按照固定的key保存值
	'''
	hero_detail = {}
	hero_id = string.atoi(toks[0])
	hero_detail['win'] = string.atoi(toks[1]) # 表示胜场数量
	hero_detail['lose'] = string.atoi(toks[2]) # 表示负场数量
	hero_data[hero_id] = hero_detail

def _init_key(key, default_value):
	if key not in hero_data:
		hero_data[key] = default_value


def update_heros(hero_list):
	'''
		批量更新英雄信息
	'''
	for hero_detail in hero_list:
		update_hero(hero_detail)

def update_hero(hero_detail):
	'''
		更新单条英雄信息
	'''
	hero_id = hero_detail['id']
	win = hero_detail['win']
	_init_key(hero_id, {'win':0, 'lose':0})
	if win == 1:
		hero_data[hero_id]['win'] += 1
	else:
		hero_data[hero_id]['lose'] += 1


def load():
	log_n('datacenter load')
	ifile = open(datapath, 'r')
	lines = ifile.readlines()
	for line in lines:
		toks = line.split('\t')
		_process(toks)
	ifile.close()

def save():
	log_n('datacenter save')
	ofile = open(datapath, 'w')
	#print 'data size: ' + str(len(hero_data))
	for hero_id, hero_detail in hero_data.items():
		line = str(hero_id) + '\t' + str(hero_detail['win']) + '\t' + str(hero_detail['lose']) + '\n'
		ofile.write(line)
	ofile.close()

