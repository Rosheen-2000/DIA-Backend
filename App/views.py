import json
from django.http import HttpResponse, JsonResponse, QueryDict
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


def deletedoc(request):
    uid = request.META.get('HTTP_TOKEN')
    uid = tools.get_uid(uid)
    if uid is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    # uid = request.POST.get('uid')
    did = request.POST.get('did')
    msg = api.remove_doc(uid, did)
    return JsonResponse({'msg': msg})

def recoverdoc(request):
    uid = request.META.get('HTTP_TOKEN')
    uid = tools.get_uid(uid)
    if uid is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    did = request.POST.get('did')
    msg = api.recover_doc(uid, did)
    # return JsonResponse({'msg':'No permission'}, status=401)
    return JsonResponse({'msg': msg})


def deletedocconfirm(request):
    uid = request.META.get('HTTP_TOKEN')
    uid = tools.get_uid(uid)
    if uid is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    did = request.POST.get('did')
    msg = api.delete_doc(uid, did)
    return JsonResponse({'msg': msg})


def my_test(request):
    uid = request.GET.get('uid')
    print(uid)
    uid = tools.get_uid(uid)
    print(uid)
    return HttpResponse('测试成功')