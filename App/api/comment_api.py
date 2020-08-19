import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse


def new_comment(user, docid, content):
    doc = Doc.objects.filter(id=docid, isdeleted=0).first()
    if doc:
        power = DocPower.objects.filter(doc=doc, member=user).first()
        if (power and power.is_commented == 1) or doc.type >= 1:
            Comment.objects.create(creator=user, content=content, doc=doc)
            msg = "Your doc '{0}' has been commented".format(doc.content.title)
            Message.objects.create(receiver=doc.creator, content=msg, mode=2, doc=doc)
            return 'true'
        return 'No permission'
    return 'doc does not exists.'

def get_comment(docid):
    doc = Doc.objects.filter(id=docid, isdeleted=0).first()
    if doc:
        comments = []
        for comment in Comment.objects.filter(doc=doc):
            ctime = datetime.datetime.strftime(comment.create_time, '%Y-%m-%d %H:%M')
            comments.append({
                'commentid':comment.id,
                'creatorname':comment.creator.name,
                'creatoravatar':comment.creator.avatar.url if comment.creator.avatar else '',
                'content':comment.content,
                'createtime':comment.create_time,
                'children':list(Comment.objects.filter(quote=comment))
            })
        return comments
    return 'doc does not exists.'

def reply(user, commentid, content):
    comment = Comment.objects.filter(id=commentid).first()
    if comment:
        if comment.doc.isdeleted:
            return 'The document is in the recycle bin.'
        if comment.quote is not None:
            return 'You cannot reply a reply-to-comment'
        power = DocPower.objects.filter(doc=comment.doc, member=user).first()
        if (power and power.is_commented == 1) or comment.doc.type >= 1: # 团队文档可评论或个人共享文档
            Comment.objects.create(creator=user, content=content, doc=comment.doc, quote=comment)
            return 'true'
        return 'No permission'
    return 'comment does not exists.'

def delete_comment(user, commentid):
    comment = Comment.objects.filter(id=commentid).first()
    if comment:
        if comment.doc.isdeleted:
            return 'The document is in the recycle bin.'
        power = DocPower.objects.filter(doc=comment.doc, member=user).first()
        if (power and power.role == 4) or comment.creator == user: # 4级文档权限和评论创建者
            comment.delete()
            return 'true'
        return 'No permission'
    return 'comment does not exists.'

