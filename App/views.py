import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from . import tools
from . import api

def add_data(request):
    tools.add_data()
    return HttpResponse('添加成功')

def login(request):
    name = request.POST.get('uname')
    pwd = request.POST.get('pwd')
    msg, value = api.login(name, pwd)
    return JsonResponse({'msg': msg, 'token': value})

def register(request):
    name = request.POST.get('uname')
    pwd = request.POST.get('pwd')
    msg, value = api.register(name, pwd)
    return JsonResponse({'msg': msg, 'token': value})

def check(request):
    name = request.POST.get('uname')
    return JsonResponse({'res': api.check(name)})