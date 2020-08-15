import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse


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
    return True, encrypt(uid)

def check(name):
    if User.objects.filter(name=name).first():
        return "Username exists."
    return 'true'

def get_user_binfo(uid):
    user = User.objects.filter(id=uid).first()
    if user is None:
        return 'Can not find by this id', '', ''
    else:
        return 'true', user.name, str(user.profile)

def get_user_ainfo(uid):
    user = User.objects.filter(id=uid).first()
    if user is None:
        return 'Can not find by this id', '', '', '', ''
    else:
        mail = user.mail if user.mail is not None else ''
        tel = user.tel if user.tel is not None else ''
        return 'true', user.name, str(user.profile), mail, tel

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

def changeMail(uid, newmail):
    user = User.objects.filter(uid = uid).first()
    if user is None:
        return 'User inexisted'
    user.mail = newmail
    user.save()
    return 'true'

def changePhoneNo(uid, newphoneno):
    user = User.objects.filter(uid = uid).first()
    if user is None:
        return 'User inexisted'
    user.tel = newphoneno
    user.save()
    return 'true'