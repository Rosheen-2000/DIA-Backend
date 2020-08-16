import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse
import time
import base64
import tempfile


def login(name, password):
    user = User.objects.filter(name=name).first()
    if user:
        if user.password == password:
            value = encrypt(user.id)
            return 'true', value
        return "Wrong Password", ''

    return "Username does not exist.", ''

def register(name, password):
    if check(name) != 'true':
        return "Username exists.", ''
    uid = User.objects.create(name=name, password=password).id
    return 'true', encrypt(uid)

def check(name):
    if User.objects.filter(name=name).first():
        return "Username exists."
    return 'true'

def get_user_basicinfo(uid):
    user = User.objects.filter(id=uid).first()
    if user is None:
        return 'Can not find by this id', '', ''
    return 'true', user.name, user.avatar.url if user.avatar else ''

def get_user_allinfo(user):
    avatar = user.avatar.url if user.avatar else ''
    mail = user.mail if user.mail else ''
    tel = user.tel if user.tel else ''
    return 'true', user.name, avatar, mail, tel

def modify_uname(user, new_name):
    # u = User.objects.filter(id=uid).first()
    if check(new_name) != 'true':
        return 'conflict'
    user.name = new_name
    user.save()
    return 'true'

def modify_pwd(user, currentpwd, newpwd):
    # user = User.objects.filter(id=uid).first()
    if user.password == currentpwd:
        user.password = newpwd
        user.save()
        return 'true'
    return 'notmatch'

def changeMail(user, newmail):
    # user = User.objects.filter(id = uid).first()
    if user is None:
        return 'User inexisted'
    user.mail = newmail
    user.save()
    return 'true'

def changePhoneNo(user, newphoneno):
    # user = User.objects.filter(id = uid).first()
    if user is None:
        return 'User inexisted'
    user.tel = newphoneno
    user.save()
    return 'true'

def change_newavatar(user, new_avatar):
    new_avatar = base64.b64decode(bytes(new_avatar, encoding='utf-8'))
    temp = tempfile.TemporaryFile()
    temp.write(new_avatar)
    user.avatar.save(time.strftime("%Y-%m-%d_%H%M%S", time.localtime())+'.jpg', temp)
    temp.close()
    return 'true'

def getTeam(uid):
    print(uid)
    teamList = []
    if not User.objects.filter(id=uid).exists():
        return {'msg':'User inexisted','teamlist':teamList}
    teamIdList = TeamMember.objects.filter(member_id = uid).values_list('team') # use teamList[i][0] to get No.i team.id
    teamNum = len(teamIdList)
    for i in range(teamNum):
        name = Team.objects.filter(id = teamIdList[i][0]).first()
        if name is None:
            return {'msg':'Team inexisted','teamlist':teamList}
        name = name.name
        teamList.append({'name':name,'id':str(teamIdList[i][0])})
    return {'msg':'true','teamlist':teamList}
