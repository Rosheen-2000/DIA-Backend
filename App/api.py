from .models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message
from .tools import encrypt, decrypt

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

def remove_doc(uid, did):
    doc = Doc.objects.filter(did=did, creator__uid=uid).first()
    if doc is not None:
        doc.isdeleted = 1
        doc.save()
        return 'true'
    else:
        return 'Remove doc field'

def recover_doc(uid, did):
    doc = Doc.objects.filter(did=did, creator__uid=uid).first()
    if doc is not None:
        doc.isdeleted = 0
        doc.save()
        return 'true'
    else:
        return 'Recover doc field'

def delete_doc(uid, did):
    print(uid, did)
    doc = Doc.objects.filter(did=did, creator__uid=uid).first()
    if doc is not None:
        doc.content.delete()
        doc.delete()
        return 'true'
    else:
        return 'Delete doc field'


