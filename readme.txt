run server:
python manage.py runserver 10.129.148.43:9999

环境部署: 

spider.py依赖了beautifulsoup和lxml
pip install beautifulsoup4
pip install lxml


花絮: 
调研Pycharm的使用. sublime还是不如IDE方便啊.


一期开发计划: 
0. 针对主页, 实现数据从数据文件中加载. [ok]
1. 针对单个英雄, 实现数据从数据文件中加载数据. [ok]
2. 补全全英雄的数据和加载. [ok]
	a) 需要爬虫来爬取数据. [ok]
	b) 按照既定的格式来直接做成数据. [ok]
3. 针对单个装备, 实现数据从文件中加载. [放到后面]
4. 补全全装备的数据和加载. [放到后面]
5. 优化title的体验 [放到后面]

完成一期上线.

二期计划:
0. 调研stream接口(https://developer.valvesoftware.com/wiki/Steam_Web_API) 主要可以实现列出比赛和比赛明细
1. 英雄维度的数据收集(更细粒度的使用情况和胜率) 
	a) 分职业比赛和路人两个大维度. 先做比赛维度. 
	b) 即某英雄在最近的比赛中, ban n次, pick n次, 获胜n次, 胜率xx, 平均比赛时间, 平均gpm, xpm, 平均伤害等.
2. 英雄维度的视频收集(优酷等源的引入)
3. 英雄维度的直播收集(通过stream平台, 判定当前主播的游戏情况, 并推送直播视频)





================关于datacenter.py================

使用datacenter.py来管理数据文件的加载和解析.
数据文件采用json格式.
导出以下几个函数用于填充模板:
1. get_mainpage_hero: 返回一个列表, 每一个元素是一个hero对象, 包括名字, 图片url, 跳转url.
2. get_detail_hero: 返回一个字典, 英雄的详细信息, 包括名字, 头像url, 各种属性, 技能等. 这个相对比较复杂了.