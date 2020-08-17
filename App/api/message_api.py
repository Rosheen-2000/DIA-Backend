import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse


def get_unread_number(user):
    return Message.objects.filter(receiver=user, is_read=False).count()

