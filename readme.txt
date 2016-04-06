run server:
python manage.py runserver 10.129.148.43:9999

环境部署: 

spider.py依赖了beautifulsoup和lxml
pip install beautifulsoup4
pip install lxml


开发计划: 
0. 针对主页, 实现数据从数据文件中加载.
1. 针对单个英雄, 实现数据从数据文件中加载数据.
2. 补全全英雄的数据和加载.


================关于datacenter.py================

使用datacenter.py来管理数据文件的加载和解析.
数据文件采用json格式.
导出以下几个函数用于填充模板:
1. get_mainpage_hero: 返回一个列表, 每一个元素是一个hero对象, 包括名字, 图片url, 跳转url.
2. get_detail_hero: 返回一个字典, 英雄的详细信息, 包括名字, 头像url, 各种属性, 技能等. 这个相对比较复杂了.