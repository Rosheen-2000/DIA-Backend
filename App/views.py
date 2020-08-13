import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
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

def new_doc(request):
    uid = request.POST.get('uid')
    title = request.POST.get('title')
    content = request.POST.get('content')
    msg, did = api.new_doc(uid, title, content)
    return JsonResponse({'msg': msg, 'docid': did})

def modify_doc_content(request):
    uid = request.POST.get('uid')
    did = request.POST.get('did')
    content = request.POST.get('content')
    return JsonResponse({'msg': api.modify_doc_content(uid, did, content)})
