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

