import json, time
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render

from . import tools
from .api import user_api, doc_api, team_api, comment_api, other_api, message_api

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


#team
def team_create(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamname = request.POST.get('teamname')
    # print(teamname)
    # teammenbers = request.POST.get('initmember')
    # print(teammenbers)
    # print('--------------------------------------------')
    ret = team_api.createTeam(user, teamname)
    return JsonResponse(ret)

def team_disband(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamid = request.POST.get('teamid')
    msg = team_api.disbandTeam(user, teamid)
    return JsonResponse({'msg': msg})

def team_getlist(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamlist = team_api.getTeamList(user)
    return JsonResponse({'teamlist': teamlist})

def get_team_info(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamid = request.GET.get('teamid')
    teamname, creatorname, creatoravatar, createtime, member = team_api.get_team_info(user, teamid)
    return JsonResponse({'teamname':teamname, 'creatorname':creatorname, \
                         'creatoravatar':creatoravatar, 'createtime':createtime, 'member':member})

def get_user_by_uname(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    uname = request.GET.get('username')
    username, avatar, userid = team_api.get_user_by_uname(uname)
    return JsonResponse({'username':username, 'avatar':avatar, 'userid':userid})

def invite(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamid = request.POST.get('teamid')
    uidList = request.POST.get('uid')
    return JsonResponse({'msg':team_api.invite(user, teamid, uidList)})

def deal_invitation(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamid = request.POST.get('teamid')
    handle = request.POST.get('handle')
    return JsonResponse({'msg':team_api.deal_invitation(user, teamid, handle)})

def remove_user(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamid = request.POST.get('teamid')
    uid = request.POST.get('uid')
    return JsonResponse({'msg':team_api.remove_user(user, teamid, uid)})


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

def reply(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    commentid = request.POST.get('commentid')
    content = request.POST.get('content')
    return JsonResponse({'msg':comment_api.reply(user, commentid, content)})

def delete_comment(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    commentid = request.POST.get('commentid')
    return JsonResponse({'msg':comment_api.delete_comment(user, commentid)})

def get_team_power(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    teamid = request.POST.get('teamid')
    power = team_api.get_power(user, teamid)
    return JsonResponse({'userPower': power})


#message
def get_unread_number(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    return JsonResponse({'num':message_api.get_unread_number(user)})

def message_getall(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    msgs = message_api.getAllMessage(user)
    return JsonResponse({'msgs': msgs})


#doc-system
def doc_desktop_file(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    files = doc_api.getDesktopFile(user)
    return JsonResponse({'files': files})

def doc_desktop_folder(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    folders = doc_api.getDesktopFolder(user)
    return JsonResponse({'folders': folders})

def doc_space_file(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamid = request.POST.get('spaceId')
    files = doc_api.getTeamFile(user, teamid)
    return JsonResponse({'files': files})

def doc_space_folder(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    teamid = request.POST.get('spaceId')
    folders = doc_api.getTeamFolder(user, teamid)
    return JsonResponse({'folders': folders})

def doc_folder_file(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    folderid = request.GET.get('folderId')
    files = doc_api.getSubFile(user, folderid)
    return JsonResponse({'files': files})

def doc_folder_folder(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg':'No permission'}, status=401)
    folderid = request.GET.get('folderId')
    folders = doc_api.getSubFolder(user, folderid)
    return JsonResponse({'folders': folders})


#etc
def add_data(request):
    tools.add_data()
    return HttpResponse('添加成功')

def request_modify_doc(request):
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    docid = request.POST.get('docid')
    msg, content, tag = other_api.request_modify_doc(user, docid)
    return JsonResponse({'msg': msg, 'content': content, 'tag': tag})

def update_doc_status(request):
    # 每次更新验证token
    user = tools.get_uid(request.META.get('HTTP_TOKEN'))
    if user is None:
        return JsonResponse({'msg': 'No permission'}, status=401)
    return JsonResponse({'msg': other_api.update_doc_status})

def check_doc_status(request):
    other_api.check_doc_status()
    return HttpResponse('check begin')


def my_test(request):
    tools.my_test()
    return HttpResponse('测试成功')


