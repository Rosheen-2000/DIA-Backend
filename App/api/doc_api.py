import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse, getPower, get_folder_power, havePowerToDeleteFolder, _deleteFolder, _recoverFolder


#doc
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
        folder = doc.father
        if folder:
            if folder.isdeleted == 1:
                doc.father = None
        doc.save()
        return 'true'
    else:
        if docp is None or docp.role < 4:
            return 'You have no permission'
        else:
            doc.isdeleted = 0
            folder = doc.father
            if folder:
                if folder.isdeleted == 1:
                    doc.father = None
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
        elif folder_id and folder.team != team:  # 非团队文件夹
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
        DocPower.objects.create(doc=doc, member=team.creator, role=4, is_commented=1) # 队长权限为4
        if team.creator != creator:
            DocPower.objects.create(doc=doc, member=creator, role=4, is_commented=1) # 创建者权限为4
        #管理员未定
    else:
        DocPower.objects.create(doc=doc, member=creator, role=4, is_commented=True)
    return 'true', str(doc.id)


def modify_doc_content(modifier, did, content):
    doc = Doc.objects.filter(id=did, isdeleted=0).first()
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
    doc = Doc.objects.filter(id=docid, isdeleted=0).first()
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
    doc = Doc.objects.filter(id=docid, isdeleted=0).first()
    if doc is None:
        return {'Title': '', 'Content': '', 'starred': False, 'isTeamDoc': False}
    power = getPower(user, doc)
    if power < 1:
        return {'Title': '', 'Content': '', 'starred': False, 'isTeamDoc': False}
    title = doc.content.title
    content = doc.content.content
    # if Favorite.objects.filter(uid=user, did=docid).exists():
    #     starred = True
    # else:
    #     starred = False
    starred = Favorite.objects.filter(uid=user, did=doc).exists()
    updateBrowse(user, doc)
    isTeamDoc = (doc.team is not None)
    return {'Title': title, 'Content': content, 'starred': starred, 'isTeamDoc': isTeamDoc}

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
        if fav.did.isdeleted:
            continue
        id = fav.did.id
        name = fav.did.content.title
        files.append({'name': name, 'id': str(id), 'starred': True})
    return files

def getBrowsedFile(user):
    files = []
    broList = Browse.objects.filter(uid=user).order_by('-create_time')
    for bro in broList:
        if bro.did.isdeleted:
            continue
        id = bro.did.id
        name = bro.did.content.title
        fav = False if Favorite.objects.filter(did=bro.did, uid=bro.uid).first() is None else True
        files.append({'name': name, 'id': str(id), 'starred': fav})
    return files

def favordoc(user, did):
    doc = Doc.objects.filter(id=did, isdeleted=0).first()
    if doc is None:
        return 'Wrong did'
    fav = Favorite.objects.filter(uid=user, did=doc).first()
    if fav:
        return 'The document has been favorited'
    else:
        Favorite.objects.create(uid=user, did=doc)
        return 'true'

def unfavordoc(user, did):
    doc = Doc.objects.filter(id=did, isdeleted=0).first()
    if doc is None:
        return 'Wrong did'
    fav = Favorite.objects.filter(uid=user, did=doc).first()
    if not fav:
        return 'The document has not been favorited'
    else:
        fav.delete()
        return 'true'

def share_to_team(user, did, tid):
    doc = Doc.objects.filter(id=did, isdeleted=0).first()
    team = Team.objects.filter(id=tid).first()
    if not doc:
        return 'The doc does not exist'
    if not team:
        return 'The team does not exist'
    team_member = TeamMember.objects.filter(member=user, team=team).first()
    role = 0 if team_member is None else team_member.role
    if role < 1:
        return 'You have no permission to share the doc'
    if doc.team is not None:
        return 'You can not share a team-doc'
    if doc.creator != user:
        return 'This doc is not yours'

    scontent = doc.content
    content = DocContent.objects.create(title=scontent.title, content=scontent.content)
    doc = Doc.objects.create(creator=user, content=content, team=team)
    Browse.objects.create(uid=user, did=doc)

    for member in TeamMember.objects.filter(team=team, role=1):
        # 普通成员默认可读权限，可评论
        DocPower.objects.create(doc=doc, member=member.member, role=1, is_commented=1)
    DocPower.objects.create(doc=doc, member=team.creator, role=4, is_commented=1)  # 队长权限为4
    if team.creator != user:
        DocPower.objects.create(doc=doc, member=user, role=4, is_commented=1)  # 创建者权限为4
    # 管理员未定
    return 'true'

def get_power(user, docid):
    doc = Doc.objects.filter(id=docid, isdeleted=0).first()
    if doc:
        power = DocPower.objects.filter(doc=doc, member=user).first()
        power = power.role if power else 0
        return power, doc.type
    return 'doc does not exists.', ''

def getCorporation(docid):
    dpList = DocPower.objects.filter(doc = docid)
    userList = [[],[],[],[],[]]
    for dp in dpList:
        name = dp.member.name
        avatar = dp.member.avatar.url if dp.member.avatar else ''
        power = dp.role
        team = dp.doc.team
        if team is None:
            teammember = False
        else:
            teamm = TeamMember.objects.filter(team=team, member=dp.member)
            teammember = False if teamm is None else True
        if power < 4:
            userList[power].append({'username': name, 'avatar': avatar, 'isTeamMember': teammember})
        else:
            userList[power].append({'username': name, 'avatar': avatar, 'isTeamMember': teammember, 'isCreator': dp.member==dp.doc.creator})
    return {'level1': userList[1], 'level2': userList[2], 'level3': userList[3], 'level4': userList[4]}

def setShareOption(user, docid, shareOption):
    if shareOption > 2 or shareOption < 0:
        return 'Power invalid'
    doc = Doc.objects.filter(id=docid, isdeleted=0).first()
    if doc is None:
        return 'Doc inexisted'
    power = getPower(user, doc)
    if power < 3:
        return 'No permission'
    doc.type = shareOption
    doc.save()
    return 'true'

def setPower(user, tarName, docid, power):
    if power < 0 or power > 3:
        return 'Power invalid'
    tar = User.objects.filter(name=tarName).first()
    if tar is None:
        return 'Target inexisted'
    doc = Doc.objects.filter(id=docid, isdeleted=0).first()
    if doc is None:
        return 'Doc inexisted'
    setterPower = getPower(user, doc)
    if setterPower < 3 or (setterPower == 3 and power == 3):
        return 'No permission'
    is_commented = (power >= 1)
    dp = DocPower.objects.filter(member=tar, doc=doc).first()
    if power == 0:
        if dp is not None:
            dp.delete()
    else:
        if dp is None:
            dp = DocPower(member=tar, doc=doc, role=power, is_commented=is_commented)
        else:
            dp.role = power
            dp.is_commented = is_commented
        dp.save()
    return 'true'


#doc-system
def getDesktopFile(user):
    files = []
    docList = Doc.objects.filter(creator = user, isdeleted = 0, father = None, team=None)
    for doc in docList:
        name = doc.content.title
        id = str(doc.id)
        starred = Favorite.objects.filter(uid = user, did = doc).exists()
        files.append({'name': name, 'id': id, 'starred': starred})
    return files

def getDesktopFolder(user):
    folders = []
    folderList = Folder.objects.filter(creator = user, isdeleted = 0, father = None, team=None)
    for folder in folderList:
        name = folder.name
        id = str(folder.id)
        folders.append({'name': name, 'id': id})
    return folders

def getTeamFile(user, teamid):
    files = []
    tmember = TeamMember.objects.filter(team=teamid, member=user).first()
    if tmember is None:
        files.append({'name': '', 'id': '', 'starred': ''})
        return files
    docList = Doc.objects.filter(team = teamid, isdeleted = 0, father = None)
    for doc in docList:
        if doc.content is None:
            continue
        name = doc.content.title
        id = str(doc.id)
        starred = Favorite.objects.filter(uid = user, did = doc).exists()
        files.append({'name': name, 'id': id, 'starred': starred})
    return files

def getTeamFolder(user, teamid):
    folders = []
    tmember = TeamMember.objects.filter(team=teamid, member=user).first()
    if tmember is None:
        folders.append({'name': '', 'id': ''})
        return folders
    folderList = Folder.objects.filter(team = teamid, isdeleted = 0, father = None)
    for folder in folderList:
        name = folder.name
        id = str(folder.id)
        folders.append({'name': name, 'id': id})
    return folders

def getSubFile(user, folderid):
    files = []
    docList = Doc.objects.filter(isdeleted = 0, father = folderid)
    for doc in docList:
        if doc.content is None:
            continue
        name = doc.content.title
        id = str(doc.id)
        starred = Favorite.objects.filter(uid = user, did = doc).exists()
        files.append({'name': name, 'id': id, 'starred': starred})
    return files

def getSubFolder(user, folderid):
    folders = []
    folderList = Folder.objects.filter(isdeleted = 0, father = folderid)
    for folder in folderList:
        name = folder.name
        id = str(folder.id)
        folders.append({'name': name, 'id': id})
    return folders

def newFolder(user, folderName, folderid, teamid):
    if folderName == '':
        folderName = '新建文件夹'
    if folderid != '':
        parentFolder = Folder.objects.filter(id = folderid).first()
        if not parentFolder:
            return 'Parent folder inexisted'
    else:
        parentFolder = None
    if teamid != '':
        team = Team.objects.filter(id = teamid).first()
        if not team:
            return 'Team inexisted'
    else:
        team = None
    # no need to judge same-name folders
    folder = Folder(name = folderName, father = parentFolder, creator = user, team = team)
    folder.save()
    return 'true'

def rename_folder(user, folderid, nname):
    folder = Folder.objects.filter(id=folderid).first()
    if folder is None:
        return 'Wrong folder id'
    folder.name = nname
    folder.modify_time = timezone.now()
    folder.save()
    return 'true'

def move_file(user, type, id, fid, tid):
    if fid == '':
        target = None
    else:
        target = Folder.objects.filter(id=fid).first()
        if target is None:
            return 'Wrong target'
    if tid == '':
        team = None
    else:
        team = Team.objects.filter(id=tid).first()
        if team is None:
            return 'Wrong team id'
        if TeamMember.objects.filter(team=team, member=user).first() is None:
            return 'You are not the member of this team'

    if type == 'file':
        doc = Doc.objects.filter(id=id).first()
        if doc is None:
            return 'Wrong file id'
        role = getPower(user, doc)
        if role < 4:
            return 'No permission'
        doc.father = target
        doc.team = team
        doc.save()
        return 'true'
    elif type == 'folder':
        folder = Folder.objects.filter(id=id).first()
        if not folder:
            return 'Wrong folder id'
        pless = get_folder_power(user, folder)
        print(pless)
        if pless != 0:
            return 'No permission'
        folder.father = target
        folder.team = team
        folder.save()
        return 'true'

def get_tree(user, teamid):
    tree = []
    if teamid != '':
        team = Team.objects.filter(id=teamid).first()
        if not team:
            return {'type': 'file', 'name': '', 'id': '', 'children': []}
    else:
        team = None
    if team:
        docs = Doc.objects.filter(team=team, isdeleted=0, father=None)
        folders = Folder.objects.filter(team=team, isdeleted=0, father=None)
    else:
        docs = Doc.objects.filter(creator=user, team=team, isdeleted=0, father=None)
        folders = Folder.objects.filter(creator=user, team=team, isdeleted=0, father=None)
    for doc in docs:
        stree = []
        dit = {'type': 'file', 'name': doc.name, 'id': str(doc.id), 'children': stree}
        tree.append(dit)
    for folder in folders:
        stree = get_sub_tree(folder)
        dit = {'type': 'folder', 'name': folder.name, 'id': str(folder.id), 'children': stree}
        tree.append(dit)
    return tree


def get_sub_tree(folder):
    tree = []
    for file in folder.child.all():
        if file.isdeleted == 1:
            continue
        if type(file) == type(Doc):
            stree=[]
            dit = {'type': 'file', 'name': file.name, 'id': str(file.id), 'children': stree}
            tree.append(dit)
        else:
            stree = get_sub_tree(file)
            dit = {'type': 'folder', 'name': file.name, 'id': str(file.id), 'children': stree}
            tree.append(dit)
    return tree

def getParentFolder(user, folderid):
    folder = Folder.objects.filter(id = folderid, isdeleted = 0).first()
    if not folder:
        return {'spaceId': '', 'spaceName': '', 'path': ''}
    if folder.team:
        spaceId = str(folder.team.id)
        spaceName = folder.team.name
    else:
        spaceId = ''
        spaceName = ''
    parent = folder.father
    path = []
    path.append({'folderId': folder.id, 'folderName': folder.name})
    while parent:
        id = str(parent.id)
        name = parent.name
        path.append({'folderId': id, 'folderName': name})
        parent = parent.father
    path.reverse()
    return {'spaceId': spaceId, 'spaceName': spaceName, 'path': path}

def deleteFolder(user, folderid):
    folder = Folder.objects.filter(id = folderid, isdeleted = 0).first()
    if not folder:
        return 'Folder inexisted'
    if not havePowerToDeleteFolder(user, folder):
        return 'no permission'
    _deleteFolder(folder)
    return 'true'

def confirmDeleteFolder(user, folderid):
    folder = Folder.objects.filter(id = folderid).first()
    if not folder:
        return 'Folder inexisted'
    if folder.isdeleted == 0:
        return 'Folder has not been deleted'
    if not havePowerToDeleteFolder(user, folder):
        return 'no permission'
    folder.delete()
    return 'true'

def recoverFolder(user, folderid):
    folder = Folder.objects.filter(id = folderid).first()
    if not folder:
        return 'Folder inexisted'
    if folder.isdeleted == 0:
        return 'Folder has not been deleted'
    if not havePowerToDeleteFolder(user, folder):
        return 'no permission'
    if folder.father and folder.father.isdeleted == 1:
        folder.father = None
    _recoverFolder(folder)
    return 'true'

def getDeletedFolder(user):
    folders = []
    folderList = Folder.objects.filter(creator = user, isdeleted = 1)
    for folder in folderList:
        name = folder.name
        id = str(folder.id)
        folders.append({'foldername': name, 'folderid': id})
    return folders

def get_detail_info(docid):
    doc = Doc.objects.filter(id=docid).first()
    if not doc:
        return '', '', '', '', '', ''
    return doc.content.title, doc.creator.name, doc.team.name if doc.team else '', \
        doc.create_time.strftime('%Y-%m-%d %H:%M:%S'), str(doc.modify_num), \
        doc.modify_time.strftime('%Y-%m-%d %H:%M:%S')
