import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse


def new_comment(user, docid, content):
    doc = Doc.objects.filter(id=docid).first()
    if doc:
        power = DocPower.objects.filter(doc=doc, member=user).first()
        if (power and power.is_commented == 1) or doc.type >= 1:
            Comment.objects.create(creator=user, content=content, doc=doc)
            return 'true'
        return 'No permission'
    return 'doc does not exists.'

def get_comment(docid):
    doc = Doc.objects.filter(id=docid).first()
    if doc:
        comments = []
        for comment in Comment.objects.filter(doc=doc):
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

