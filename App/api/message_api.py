import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse


def get_unread_number(user):
    return Message.objects.filter(receiver=user, is_read=False).count()

def getAllMessage(user):
    msgs = []
    msgList = Message.objects.filter(receiver = user)
    for msg in msgList:
        mid = str(msg.id)
        msgtype = msg.mode
        isread = msg.is_read
        content = msg.content
        teamid = (str(msg.team.id) if (msg.team is not None) else '')
        docid = (str(msg.doc.id) if (msg.doc is not None) else '')
        createtime = msg.create_time.strftime('%Y-%m-%d %H:%M')
        msgs.append({'mid': mid, 'msgtype': msgtype, 'isread': isread, 'content': content, 'teamid': teamid, 'docid': docid, 'createtime': createtime})
    return msgs

def create_normal_message(uname, content):
    user = User.objects.filter(name=uname).first()
    if user is None:
        return
    Message.objects.create(receiver=user, content=content, mode=0)

def offline_message(user):
    # user = User.objects.filter(name=uname).first()
    # if user is None:
    #     return 0
    msgs = Message.objects.filter(receiver=user, is_send=0)
    num = msgs.count()
    for msg in msgs:
        msg.is_send = 1
        msg.save()
    return num

def online_message(user):
    # user = User.objects.filter(name=uname).first()
    # if user is None:
    #     return None
    msg = Message.objects.filter(receiver=user, is_send=0).first()
    if msg is None:
        return {'basicmsg':0, 'mid':'', 'msgtype':0, 'content':'',
               'teamid':'', 'docid':'', 'createtime':''}
    else:
        ctime = datetime.datetime.strftime(msg.create_time, '%Y-%m-%d %H:%M')
        dit = {'basicmsg':0, 'mid':str(msg.id), 'msgtype':msg.mode, 'content':msg.content,
               'teamid':str(msg.team), 'docid':str(msg.doc), 'createtime':ctime}
        msg.is_send = 1
        msg.save()
        return dit

def changeStatus(user, mid, isread):
    msg = Message.objects.filter(id = mid).first()
    if not msg:
        return 'Message inexisted'
    if msg.receiver != user:
        return 'This is not your message'
    msg.is_read = isread
    msg.save()
    return 'true'

