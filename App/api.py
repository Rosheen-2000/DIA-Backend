import datetime

from django.utils import timezone

from .models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message
from .tools import encrypt, decrypt, updateBrowse


def login(name, password):
    user = User.objects.filter(name=name).first()
    if user:
        if user.password == password:
            value = encrypt(user.uid)
            return 'true', value
        return "Wrong Password", ''

    return "Username does not exist.", ''

def register(name, password):
    if check(name) != 'true':
        return "Username exists.", ''
    uid = User.objects.create(name=name, password=password).uid
    return True, encrypt(uid)

def check(name):
    if User.objects.filter(name=name).first():
        return "Username exists."
    return 'true'

def modify_uname(uid, new_name):
    u = User.objects.filter(uid=uid).first()
    u.name = new_name
    u.save()
    return 'true'

def modify_pwd(uid, currentpwd, newpwd):
    user = User.objects.filter(uid=uid).first()
    if user.password == currentpwd:
        user.password = newpwd
        user.save()
        return 'true'
    return 'wrong password'

def remove_doc(uid, did):
    doc = Doc.objects.filter(did=did).first()
    if doc is not None:
        doc.isdeleted = 1
        doc.save()
        return 'true'
    else:
        return 'Remove doc failed'

def recover_doc(uid, did):
    doc = Doc.objects.filter(did=did).first()
    if doc is not None:
        doc.isdeleted = 0
        doc.save()
        return 'true'
    else:
        return 'Recover doc failed'

def delete_doc(uid, did):
    print(uid, did)
    doc = Doc.objects.filter(did=did).first()
    if doc is not None:
        doc.content.delete()
        doc.delete()
        return 'true'
    else:
        return 'Delete doc failed'

def new_doc(uid, title, template_id):
    template = DocTemplate.objects.filter(tid=template_id).first()
    if template:
        creator = User.objects.get(uid=uid)
        # content = template.content
        # print(template.objects.value())
        # print(template.title)
        # print(template.content)
        content = DocContent(title=title, content=template.content.content)
        content.save()
        # content.title = title
        doc = Doc.objects.create(creator=creator, content=content)
        Browse.objects.create(uid=creator, did=doc)
        return 'true', str(doc.did)
    return 'Template does not exists.', None

def modify_doc_content(uid, did, content):
    modifier = User.objects.filter(uid=uid).first()
    doc = Doc.objects.filter(did=did).first()
    if modifier:
        if doc:
            doc.content.content = content
            doc.content.save()
            doc.modify_num += 1
            doc.modify_people = modifier
            doc.modify_time = timezone.now()
            Browse.objects.create(uid=modifier, did=doc)
            return 'true'
        return 'did does not exists'
    return 'uid does not exists.'

def get_all_templates():
    templates = []
    for template in DocTemplate.objects.all():
        templates.append({'name':template.name, 'id':str(template.tid)})
    return templates


def get_user_binfo(uid):
    user = User.objects.filter(uid=uid).first()
    if user is None:
        return 'Can not find by this id', '', ''
    else:
        return 'true', user.name, user.profile


def modifyDocTitle(uid, docid, title):
    doc = Doc.objects.filter(did = docid).first()
    if doc is None:
        return 'Doc inexisted'
    doc.content.title = title
    doc.content.save()
    doc.create_time = datetime.datetime.now()   # actually it's modify_time
    doc.modify_num += 1
    # doc.modify_people
    # Browse
    doc.save()
    return 'true'

def getDocContent(uid, docid):
    # print(docid)
    doc = Doc.objects.filter(did=docid).first()
    # print(type(doc.did))
    if doc is None:
        return {'Title': '', 'Content': ''}
        # return 'Doc inexisted'
    title = doc.content.title
    content = doc.content.content
    updateBrowse(uid, docid)
    return {'Title':title, 'Content':content}

def get_own_file(uid):
    user = User.objects.filter(uid=uid).first()
    # print(user)
    res = []
    if user:
        docs = Doc.objects.filter(creator=user)
        for doc in docs:
            res.append({'name':doc.content.title, 'id': str(doc.did)})
        # return res
    return res

def get_trash_file(uid):
    user = User.objects.filter(uid=uid).first()
    # print(user)
    res = []
    if user:
        docs = Doc.objects.filter(creator=user, isdeleted=1)
        for doc in docs:
            res.append({'name':doc.content.title, 'id': str(doc.did)})
        # return res
    return res

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
