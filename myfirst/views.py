#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	return render(request, 'main.html')

def detail(request):
	return render(request, 'detail.html')
