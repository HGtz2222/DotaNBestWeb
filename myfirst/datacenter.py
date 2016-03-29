#coding:utf-8
import data.mainpage_hero as m_heros
import data.detail_hero as d_heros
def get_mainpage_hero():
	return m_heros.data

def get_detail_hero(name):
	return d_heros.data[name]