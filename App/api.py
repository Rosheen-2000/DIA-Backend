from django.utils import timezone

from .models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message
from .tools import encrypt, decrypt

def login(name, password):
    user = User.objects.filter(name=name).first()
    if user:
        if user.password == password:
            value = encrypt(user.password)
            return 'true', value
        return 'Wrong Password', ''

    return 'Username does not exist.', ''

def register(name, password):
    if check(name) != 'true':
        return 'Username exists.', ''
    User.objects.create(name=name, password=password)
    return 'true', encrypt(password)

def check(name):
    if User.objects.filter(name=name).first():
        return 'Username exists.'
    return 'true'

def new_doc(uid, title, content):
    user = User.objects.filter(uid=uid).first()
    if user:
        content = DocContent.objects.create(title=title, content=content)
        return 'true', Doc.objects.create(creator=user, content=content).did
    return 'uid does not exists.', None

def modify_doc_content(uid, did, content):
    modifier = User.objects.filter(uid=uid).first()
    doc = Doc.objects.filter(did=did).first()
    if modifier:
        if doc:
            doc.content = content
            doc.modify_num += 1
            doc.modify_people = modifier
            doc.modify_time = timezone.now()
            return 'true'
        return 'did does not exists'
    return 'uid does not exists.'
