import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse, getPower


def remove_doc(user, did):
    doc = Doc.objects.filter(id=did, isdeleted=0).first()
    if doc is None:
        return 'Wrong did'

    docp = DocPower.objects.filter(member_id=user.id, doc_id=did).first()
    # team_leader = None if doc.team == None else doc.team.creator
    # print(docp.id)
    # print(uid)
    # print(doc.creator.uid)
    if user.id == doc.creator.id:
        doc.isdeleted = 1
        doc.save()
        return 'true'
    else:
        if docp is None or docp.role < 4:
            return 'You have no permission'
        else:
            doc.isdeleted = 1
            doc.save()
            return 'true'


def recover_doc(user, did):
    doc = Doc.objects.filter(id=did, isdeleted=1).first()
    if doc is None:
        return 'Wrong did'

    docp = DocPower.objects.filter(member_id=user.id, doc_id=did).first()
    # team_leader = None if doc.team == None else doc.team.creator
    # print(docp.id)
    # print(uid)
    # print(doc.creator.uid)
    if user.id == doc.creator.id:
        doc.isdeleted = 0
        doc.save()
        return 'true'
    else:
        if docp is None or docp.role < 4:
            return 'You have no permission'
        else:
            doc.isdeleted = 0
            doc.save()
            return 'true'

def delete_doc(user, did):
    doc = Doc.objects.filter(id=did, isdeleted=1).first()
    if doc is None:
        return 'Wrong did'

    docp = DocPower.objects.filter(member_id=user.id, doc_id=did).first()
    # team_leader = None if doc.team == None else doc.team.creator
    # print(docp.id)
    # print(uid)
    # print(doc.creator.uid)
    if user.id == doc.creator.id:
        doc.content.delete()
        return 'true'
    else:
        if docp is None or docp.role < 4:
            return 'You have no permission'
        else:
            doc.content.delete()
            return 'true'

def new_doc(creator, title, template_id, folder_id, team_id):
    template = DocTemplate.objects.filter(id=template_id).first()
    if not template:
        return 'Template does not exists.', ''
    folder = None # 默认为根目录
    team = None # 默认为个人文档
    if folder_id:
        folder = Folder.objects.filter(id=folder_id).first()
        if not folder: # folder_id不存在
            return 'Folder does not exists.', ''
    if team_id:
        team = Team.objects.filter(id=team_id).first()
        if not team: # team_id不存在
            return 'Team does not exists.', ''
        elif not TeamMember.objects.filter(team=team, member=creator).exists(): # 非团队成员
            return 'No permisson to create documents in this team.', ''
        elif TeamMember.objects.filter(team=team, member=creator).first().role < 1:
            return 'No permisson to create documents in this team.', ''
        elif folder.team != team: # 非团队文件夹
            return 'Folder does not belong to this team.', ''
        # 黑名单未定，判断已加上
    elif folder and folder.team is not None: # 非个人文件夹
        return 'This is a team folder.', ''
    content = DocContent.objects.create(title=title, content=template.content.content)
    doc = Doc.objects.create(creator=creator, content=content, father=folder, team=team)
    Browse.objects.create(uid=creator, did=doc)
    if team:
        for member in TeamMember.objects.filter(team=team, role=1):
            # 普通成员默认可读权限，可评论
            DocPower.objects.create(doc=doc, member=member.member, role=1, is_commented=1)
        DocPower.objects.create(doc=doc, member=team.creator, role=4) # 队长权限为4
        if team.creator != creator:
            DocPower.objects.create(doc=doc, member=creator, role=4) # 创建者权限为4
        #管理员未定
    return 'true', str(doc.id)


def modify_doc_content(modifier, did, content):
    doc = Doc.objects.filter(id=did).first()
    if doc:
        # doc_power = DocPower.objects.filter(doc=doc, member=modifier).first()
        authority = getPower(modifier, doc)
        if authority < 2:
            return 'No permission to modify.'
        doc.content.content = content
        doc.content.save()
        doc.modify_num += 1
        doc.modify_people = modifier
        doc.modify_time = timezone.now()
        updateBrowse(modifier, doc)
        return 'true'
    return 'Doc does not exists'

def get_all_templates():
    templates = []
    for template in DocTemplate.objects.all():
        templates.append({'name':template.content.title, 'id':str(template.id)})
    return templates

def modifyDocTitle(user, docid, title):
    doc = Doc.objects.filter(id=docid).first()
    if doc is None:
        return 'Doc inexisted'
    power = getPower(user, doc)
    if power < 2:
        return 'No permission'
    doc.content.title = title
    doc.content.save()
    doc.modify_time = datetime.datetime.now()
    doc.modify_num += 1
    # doc.modify_people
    # Browse
    doc.save()
    return 'true'

def getDocContent(user, docid):
    doc = Doc.objects.filter(id=docid).first()
    if doc is None:
        return {'Title': '', 'Content': '', 'starred': False}
    power = getPower(user, doc)
    if power < 1:
        return {'Title': '', 'Content': '', 'starred': False}
    title = doc.content.title
    content = doc.content.content
    if Favorite.objects.filter(uid=user, did=docid).exists():
        starred = True
    else:
        starred = False
    updateBrowse(user, doc)
    return {'Title': title, 'Content': content, 'starred': starred}

def get_own_file(user):
    # user = User.objects.filter(uid=uid).first()
    # print(user)
    res = []
    if user:
        docs = Doc.objects.filter(creator=user, isdeleted=0)
        for doc in docs:
            isfav = False if Favorite.objects.filter(uid=user, did=doc).first() is None else True
            res.append({'name':doc.content.title, 'id': str(doc.id), 'starred': isfav})
        # return res
    return res

def get_trash_file(user):
    # user = User.objects.filter(uid=uid).first()
    # print(user)
    res = []
    if user:
        docs = Doc.objects.filter(creator=user, isdeleted=1)
        for doc in docs:
            res.append({'name':doc.content.title, 'id': str(doc.id)})
        # return res
    return res

def getFavoriteFile(user):
    files = []
    favList = Favorite.objects.filter(uid=user).order_by('-create_time')
    for fav in favList:
        id = fav.did.id
        name = fav.did.content.title
        files.append({'name': name, 'id': str(id), 'starred': True})
    return files

def getBrowsedFile(user):
    files = []
    broList = Browse.objects.filter(uid=user).order_by('-create_time')
    for bro in broList:
        id = bro.did.id
        name = bro.did.content.title
        fav = False if Favorite.objects.filter(did=bro.did, uid=bro.uid).first() is None else True
        files.append({'name': name, 'id': str(id), 'starred': fav})
    return files

def favordoc(user, did):
    doc = Doc.objects.filter(id=did).first()
    if doc is None:
        return 'Wrong did'
    fav = Favorite.objects.filter(uid=user, did=doc)
    if fav:
        return 'Document has been favorited'
    else:
        Favorite.objects.create(uid=user, did=doc)
        return 'true'

# def unfavordoc(user, did):
#     doc = Doc.objects