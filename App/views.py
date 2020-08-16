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
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    uid = request.POST.get('uid')
    uid = uid if uid else user.id
    msg, uname, avatar = user_api.get_user_basicinfo(uid)
    return JsonResponse({'msg': msg, 'uname':uname, 'avatar':avatar})

def userinfo_all(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    msg, uname, avatar, mail, tel = user_api.get_user_allinfo(user)
    return JsonResponse({'msg': msg, 'uname':uname, 'avatar':avatar, 'mail':mail, 'phoneno':tel})

def getteam(request):
    uid = request.GET.get('uid')
    if uid=='':
        uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
        if uid is None:
            return JsonResponse({'msg': 'No permission'}, status=401)
        uid = uid.id
    ret = user_api.getTeam(uid)
    return JsonResponse(ret)

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
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    newmail = request.POST.get('newmail')
    msg = user_api.changeMail(user, newmail)
    return JsonResponse({'msg':msg})

def changephoneno(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    newphoneno = request.POST.get('newphoneno')
    msg = user_api.changePhoneNo(user, newphoneno)
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
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    title = request.POST.get('title')
    template_id = request.POST.get('template')
    folder_id = request.POST.get('folderId')
    team_id = request.POST.get('spaceId')
    msg, did = doc_api.new_doc(user, title, template_id, folder_id, team_id)
    return JsonResponse({'msg': msg, 'docid': did})

def modify_doc_content(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    did = request.POST.get('did')
    content = request.POST.get('content')
    return JsonResponse({'msg': doc_api.modify_doc_content(user, did, content)})

def get_template(request):
    return JsonResponse({'templates': doc_api.get_all_templates()})

def modifydoctitle(request):
    uid = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if uid is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    docid = request.POST.get('docid')
    title = request.POST.get('title')
    msg = doc_api.modifyDocTitle(uid, docid, title)
    return JsonResponse({'msg':msg})

def getdoccontent(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    docid = request.POST.get('_docid')
    # print(type(docid))
    ret = doc_api.getDocContent(user, docid)
    return JsonResponse(ret)

def doc_own_file(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    ret = doc_api.get_own_file(user)
    return JsonResponse({'files': ret})

def doc_trash_file(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    ret = doc_api.get_trash_file(user)
    return JsonResponse({'files': ret})

def doc_favorites_file(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    files = doc_api.getFavoriteFile(user)
    return JsonResponse({'files': files})

def doc_used_file(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    files = doc_api.getBrowsedFile(user)
    return JsonResponse({'files': files})

def favordoc(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    did = request.POST.get('did')
    msg = doc_api.favordoc(user, did)
    return JsonResponse({'msg': msg})

def unfavordoc(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    did = request.POST.get('did')
    msg = doc_api.unfavordoc(user, did)
    return JsonResponse({'msg': msg})

def sharetoteam(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    did = request.POST.get('docid')
    teamid = request.POST.get('teamid')
    msg = doc_api.share_to_team(user, did, teamid)
    return JsonResponse({'msg': msg})

def get_power(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    docid = request.GET.get('docid')
    userPower, shareProperty = doc_api.get_power(user, docid)
    return JsonResponse({'userPower':userPower, 'shareProperty':shareProperty})

def get_corporation(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    docid = request.GET.get('docid')
    ret = doc_api.getCorporation(docid)
    return JsonResponse(ret)

def set_share_option(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    docid = request.POST.get('docid')
    try:
        shareOption = int(request.POST.get('shareOption')) # try-catch
        msg = doc_api.setShareOption(user, docid, shareOption)
        return JsonResponse({'msg': msg})
    except:
        return JsonResponse({'msg': 'Wrong power'})

def set_power(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    tarName = request.POST.get('username')
    docid = request.POST.get('docid')
    try:
        power = int(request.POST.get('power')) # try-catch
        msg = doc_api.setPower(user, tarName, docid, power)
        return JsonResponse({'msg': msg})
    except:
        return JsonResponse({'msg': 'Wrong power'})


# comment
def new_comment(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    docid = request.POST.get('docid')
    content = request.POST.get('content')
    return JsonResponse({'msg':comment_api.new_comment(user, docid, content)})

def get_comment(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    docid = request.GET.get('docid')
    comments = comment_api.get_comment(docid)
    return JsonResponse({'comments':comments})


#etc
def add_data(request):
    tools.add_data()
    return HttpResponse('添加成功')


def my_test(request):
    tools.my_test()
    return HttpResponse('测试成功')

