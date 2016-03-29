#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import datacenter as dc
# Create your views here.
def index(request):
	return render(request, 'main.html', {'data':dc.get_mainpage_hero()})

def detail(request):
	heroid = request.GET['id']
	hero = dc.get_detail_hero(heroid)
	return render(request, 'detail.html', {'hero':hero})
