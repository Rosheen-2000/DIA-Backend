import json
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render

from . import tools
from .api import user_api, doc_api, team_api, comment_api, other_api

# user
def login(request):
    name = request.POST.get('uname')
    pwd = request.POST.get('pwd')
    msg, value = user_api.login(name, pwd)
    return JsonResponse({'msg': msg, 'token': value})

def register(request):
    name = request.POST.get('uname')
    pwd = request.POST.get('pwd')
    msg, value = user_api.register(name, pwd)
    return JsonResponse({'msg': msg, 'token': value})

def check(request):
    name = request.POST.get('uname')
    return JsonResponse({'res': user_api.check(name)})

def userinfo_basic(request):
    uid = request.POST.get('uid')
    if uid == '':
        uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
        if uid is None:
            return JsonResponse({'msg': 'No permission'}, status=401)
        else:
            uid = uid.id
    msg, uname, prof = user_api.get_user_binfo(uid)
    return JsonResponse({'msg': msg, 'uname':uname, 'avatar':prof})

def userinfo_all(request):
    uid = request.POST.get('uid')
    if not uid:
        user = tools.get_uid(request.META.get('HTTP_TOKEN'))
        if user is None:
            return JsonResponse({'msg':'No permission'}, status=401)
        msg, uname, avatar, mail, tel = user_api.get_user_ainfo(user)
        return JsonResponse({'msg': msg, 'uname':uname, 'avatar':avatar, 'mail':mail, 'phoneno':tel})
    return 'uid not null'

def modify_uname(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    new_name = request.POST.get('newname')
    return JsonResponse({'msg': user_api.modify_uname(uid, new_name)})

def modify_pwd(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    currentpwd = request.POST.get('currentpwd')
    newpwd = request.POST.get('newpwd')
    return JsonResponse({'msg': user_api.modify_pwd(user, currentpwd, newpwd)})

def changemail(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    newmail = request.POST.get('newmail')
    msg = user_api.changeMail(uid, newmail)
    return JsonResponse({'msg':msg})

def changephoneno(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    newphoneno = request.POST.get('newphoneno')
    msg = user_api.changePhoneNo(uid, newphoneno)
    return JsonResponse({'msg':msg})

def change_avatar(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    new_avatar = request.POST.get('newavatar')
    msg = user_api.change_newavatar(user, new_avatar)
    return JsonResponse({'msg':msg})


# doc
def deletedoc(request):
    uid = request.META.get('HTTP_TOKEN')
    user = tools.get_uid(uid)
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    # uid = request.POST.get('uid')
    did = request.POST.get('did')
    msg = doc_api.remove_doc(user, did)
    return JsonResponse({'msg': msg})

def recoverdoc(request):
    uid = request.META.get('HTTP_TOKEN')
    user = tools.get_uid(uid)
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    did = request.POST.get('did')
    msg = doc_api.recover_doc(user, did)
    # return JsonResponse({'msg':'No permission'}, status=401)
    return JsonResponse({'msg': msg})


def deletedocconfirm(request):
    uid = request.META.get('HTTP_TOKEN')
    user = tools.get_uid(uid)
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    did = request.POST.get('did')
    msg = doc_api.delete_doc(user, did)
    return JsonResponse({'msg': msg})

def new_doc(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if not uid:
        return JsonResponse({'msg': 'No permisson'}, status=401)
    title = request.POST.get('title')
    template_id = request.POST.get('template')
    msg, did = doc_api.new_doc(uid, title, template_id)
    return JsonResponse({'msg': msg, 'docid': did})

def modify_doc_content(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if not uid:
        return JsonResponse({'msg': 'No permisson'}, status=401)
    did = request.POST.get('did')
    content = request.POST.get('content')
    return JsonResponse({'msg': doc_api.modify_doc_content(uid, did, content)})

def get_template(request):
    return JsonResponse({'templates': doc_api.get_all_templates()})

def modifydoctitle(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg':'No permission'}, status = 401)
    docid = request.POST.get('docid')
    title = request.POST.get('title')
    msg = doc_api.modifyDocTitle(uid, docid, title)
    return JsonResponse({'msg':msg})

def getdoccontent(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg':'No permission'}, status = 401)
    docid = request.GET.get('_docid')
    # print(type(docid))
    ret = doc_api.getDocContent(uid, docid)
    return JsonResponse(ret)

def doc_own_file(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    ret = doc_api.get_own_file(uid)
    return JsonResponse(ret, safe=False)


def doc_trash_file(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    ret = doc_api.get_trash_file(uid)
    return JsonResponse(ret, safe=False)


#etc
def add_data(request):
    tools.add_data()
    return HttpResponse('添加成功')

def my_test(request):
    tools.my_test()
    return HttpResponse('测试成功')
