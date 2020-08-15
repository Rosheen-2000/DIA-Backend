import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse


def remove_doc(user, did):
    doc = Doc.objects.filter(did=did, isdeleted=0).first()
    if doc is None:
        return 'Worry did'

    docp = DocPower.objects.filter(member_id=user.id, doc__did=did).first()
    # print(docp.id)
    # print(uid)
    # print(doc.creator.uid)
    if user.id == doc.creator.uid:
        doc.isdeleted = 1
        doc.save()
        return 'true'
    else:
        if docp is None or docp.role < 3:
            return 'You have no permission'
        else:
            doc.isdeleted = 1
            doc.save()
            return 'true'

def recover_doc(user, did):
    doc = Doc.objects.filter(did=did, isdeleted=1).first()
    if doc is None:
        return 'Worry did'

    docp = DocPower.objects.filter(member_id=user.id, doc__did=did).first()
    # print(docp.id)
    # print(uid)
    # print(doc.creator.uid)
    if user.id == doc.creator.uid:
        doc.isdeleted = 0
        doc.save()
        return 'true'
    else:
        if docp is None or docp.role < 3:
            return 'You have no permission'
        else:
            doc.isdeleted = 0
            doc.save()
            return 'true'

def delete_doc(user, did):
    doc = Doc.objects.filter(did=did, isdeleted=1).first()
    if doc is None:
        return 'Worry did'

    docp = DocPower.objects.filter(member_id=user.id, doc__did=did).first()
    # print(docp.id)
    # print(uid)
    # print(doc.creator.uid)
    if user.id == doc.creator.uid:
        doc.content.delete()
        # doc.save()
        return 'true'
    else:
        if docp is None or docp.role < 3:
            return 'You have no permission'
        else:
            doc.content.delete()
            return 'true'

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
        docs = Doc.objects.filter(creator=user, isdeleted=0)
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