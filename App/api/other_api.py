import datetime

from django.utils import timezone
from django.conf import settings

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse, getPower

def offline_message(uname):
    user = User.objects.filter(name=uname).first()
    if user is None:
        return 0
    msgs = Message.objects.filter(receiver=user, is_send=0)
    num = msgs.count()
    for msg in msgs:
        msg.is_send = 1
        msg.save()
    return num

def online_message(uname):
    user = User.objects.filter(name=uname).first()
    if user is None:
        return None
    msg = Message.objects.filter(receiver=user, is_send=0).first()
    if msg is None:
        return None
    else:
        dit = {'basicmsg':0, 'mid':msg.id, 'msgtype':msg.mode, 'content':msg.content,
               'teamid':str(msg.team), 'docid':str(msg.doc), 'createtime':msg.create_time}
        msg.is_send = 1
        msg.save()
        return dit

def request_modify_doc(user, docid):
    doc = Doc.objects.filter(id=docid).first()
    if not doc:
        return 'Document not found.', ''
    if getPower(user, doc) < 2:
        return 'No permisson to modify.', ''
    if doc.edit_status: # 不允许其他用户包括正在修改的用户尝试再次修改
        return 'Being modified...', ''
    doc.edit_status = 1
    doc.save()
    doc_status = DocStatus.objects.create(user=user, doc=doc)
    settings.EDITING_DOC[doc_status.id] = doc_status # 伪全局字典维护所有写状态文件
    return 'true', doc_status.id

def update_doc_status(tag):
    if settings.editing_doc.get(tag):
        # 跳过数据库，仅在字典中更新？
        settings.editing_doc[tag].time = datetime.datetime.now()
        return 'true'
    return 'Tag not found.'

def check_doc_status():
    dic = settings.editing_doc
    update_cycle = datetime.timedelta(seconds=2)
    while True:
        ctime = datetime.datetime.now()
        for doc_status in dic.values():
            if ctime - doc_status.time > update_cycle:
                DocStatus.objects.get(id=doc_status.id).delete()
                del dic[doc_status.id]
                doc = Doc.objects.get(id=doc_status.doc.id)
                doc.edit_status = 0
                doc.save()

def query_doc_status(user, docid):
    doc = Doc.objects.filter(id=docid).first()
    if not doc:
        return 'Document not found.', '', ''
    if getPower(user, doc) < 2:
        return 'No permission.'
    if doc.edit_status:
        return 'Being modified...', 1, ''
    
    docs = DocStatus.objects.filter(doc=doc).first()
    if docs is None:
        DocStatus.objects.create(doc=doc, user=user)

    return 'true', 0, DocStatus.objects.get(doc=doc).user.name

def direct_quit(tag):
    doc_status = settings.editing_doc[tag]
    del settings.editing_doc[tag]
    DocStatus.objects.get(id=doc_status.id).delete()
    doc = Doc.objects.get(id=doc_status.doc.id)
    doc.edit_status = 0
    doc.save()

