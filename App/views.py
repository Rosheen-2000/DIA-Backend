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


def new_doc(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if not uid:
        return JsonResponse({'msg': 'No permisson'}, status=401)
    title = request.POST.get('title')
    template_id = request.POST.get('template')
    msg, did = api.new_doc(uid, title, template_id)
    return JsonResponse({'msg': msg, 'docid': did})

def modify_doc_content(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if not uid:
        return JsonResponse({'msg': 'No permisson'}, status=401)
    did = request.POST.get('did')
    content = request.POST.get('content')
    return JsonResponse({'msg': api.modify_doc_content(uid, did, content)})

def get_template(request):
    return JsonResponse({'templates': api.get_all_templates()})



def modifydoctitle(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg':'No permission'}, status = 401)
    docid = request.POST.get('docid')
    title = request.POST.get('title')
    msg = api.modifyDocTitle(uid, docid, title)
    return JsonResponse({'msg':msg})

def getdoccontent(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg':'No permission'}, status = 401)
    docid = request.POST.get('_docid')
    # print(type(docid))
    ret = api.getDocContent(uid, docid)
    return JsonResponse(ret)

def my_test(request):
    uid = request.GET.get('uid')
    print(uid)
    uid = tools.get_uid(uid)
    print(uid)
    return HttpResponse('测试成功')


def doc_own_file(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    ret = api.get_own_file(uid)
    return JsonResponse(ret, safe=False)


def doc_trash_file(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    ret = api.get_trash_file(uid)
    return JsonResponse(ret, safe=False)