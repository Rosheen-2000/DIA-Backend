import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse, get_avatar_url


def createTeam(user, teamname):
    msg = ''
    teamid = ''
    if Team.objects.filter(name = teamname).exists():
        msg = 'Team exists'
    else:
        # print(teamname)
        # print(members)
        team = Team(name = teamname, creator = user, member_num = 1)
        team.save()
        teamm = TeamMember(team=team, member=user, role=2)
        teamm.save()
        msg = 'true'
        teamid = str(Team.objects.filter(name=teamname).first().id)
        # for member in members:
        #     print(member)
        #     invite(user, team.id, member)
    return {'msg': msg, 'teamid': teamid}

def disbandTeam(user, teamid):
    team = Team.objects.filter(id = teamid).first()
    if team is None:
        return 'Team inexisted'
    if user != team.creator:
        return 'No permission'
    # comment blacklist
    team.delete()
    return 'true'

def getTeamList(user):
    teamList = []
    tmList = TeamMember.objects.filter(member = user)
    for tm in tmList:
        if tm.team is None:
            continue
        id = str(tm.team.id)
        name = tm.team.name
        teamList.append({'teamid': id, 'teamname': name})
    return teamList

def get_team_info(user, teamid):
    team = Team.objects.filter(id=teamid).first()
    if not team:
        return '', '', '', '', ''
    tmember = TeamMember.objects.filter(team=teamid, member=user).first()
    if tmember is None:
        return '', '', '', '', ''
    # print(tmember.id)
    ctime = datetime.datetime.strftime(team.create_time, '%Y-%m-%d')
    members = []
    for member in TeamMember.objects.filter(team=team):
        if member.member is None:
            continue
        members.append({'uid':str(member.member.id), 'uname':member.member.name,
                        'useravatar':get_avatar_url(member.member)})
    return team.name, team.creator.name, get_avatar_url(team.creator), \
           ctime, members

def get_user_by_uname(uname):
    user = User.objects.filter(name=uname).first()
    if not user:
        return '', '', ''
    return user.name, get_avatar_url(user), user.id

def invite(user, teamid, uidList):
    team = Team.objects.filter(id=teamid).first()
    # print(teamid)
    if not team:
        return 'Team does not exist.'
    if user != team.creator:  # 暂定仅队长有权邀请新成员
        return 'No permission to invite.'
    cnt = 0
    for uid in uidList:
        invitee = User.objects.filter(id=uid).first()
        if not invitee:
            # return 'The invitee does not exist.'
            continue
        team_member = TeamMember.objects.filter(team=team, member=invitee).first()
        if team_member:
            # return 'This person is already in the team'
            continue
        content = '叮咚，您刚刚收到了一份来自队伍‘{0}’的入队邀请(●ˇ∀ˇ●)'.format(team.name)  # 邀请消息文本格式？
        Message.objects.create(team=team, content=content, receiver=invitee, mode=1)
        cnt += 1
    if cnt == len(uidList):
        return 'true'
    elif cnt == 0:
        return 'false'
    else:
        return 'warn'

def deal_invitation(user, teamid, handle):
    team = Team.objects.filter(id=teamid).first()
    if not team:
        return 'The team does not exist.'
    if handle not in ('true', 'false'):
        return 'Handle type error.'
    message = Message.objects.filter(team=team, receiver=user, mode=1).first()
    if not message:
        return 'The invitation does not exist.'
    if message.is_read: # 防止重复处理
        return 'The invitation has been dealt.'
    tmember = TeamMember.objects.filter(team=team, member=user).first()
    if tmember:
        return 'You are already the team member'
    message.is_read = True
    message.save()
    if handle == 'true':
        TeamMember.objects.create(team=team, member=user, role=1)
        # 给予当前团队文档权限
        for doc in Doc.objects.filter(team=team): # 包含回收站中的文档
            docpower = DocPower.objects.filter(doc=doc, member=user).first()
            if not docpower:
                DocPower.objects.create(doc=doc, member=user, role=1, is_commented=1)
            #     docpower.role = 1
            #     docpower.is_commented = 1
            #     docpower.save()
            # else:
            #     DocPower.objects.create(doc=doc, member=user, role=1, is_commented=1)
    # 生成处理结果消息
    content = '对{0}的入队邀请被{1}啦'.format(user.name, '同意' if handle == 'true' else '拒绝')
    Message.objects.create(content=content, receiver=team.creator, mode=0)
    return 'true'

def remove_user(handler, teamid, uid):
    team = Team.objects.filter(id=teamid).first()
    if not team:
        return 'The team does not exist.'
    user = User.objects.filter(id=uid).first()
    if not User:
        return 'The user does not exist.'
    if team.creator != handler: # 仅队长可删
        return 'No permission to remove member.'
    team_member = TeamMember.objects.filter(team=team, member=user).first()
    if not team_member:
        return 'The user is not in the team.'
    for doc in Doc.objects.filter(creator=user, team=team): # 直接删除该用户所有团队文档
        doc.delete()
    team_member.delete()
    for docpower in DocPower.objects.filter(member=user, doc__team=team):
        docpower.delete()
    Message.objects.create(receiver=user, content='You were kicked out of the team.')
    return 'true'

def get_power(user, teamid):
    team = Team.objects.filter(id=teamid).first()
    if not team:
        return 0
    teampower = TeamMember.objects.filter(member=user, team=team).first()
    power = 0 if teampower is None else teampower.role
    return power

def quit_team(user, teamid):
    team = Team.objects.filter(id=teamid).first()
    if not team:
        return 'Wrong team id'
    if user == team.creator:
        return 'The captain cannot leave the team, you can choose to disband the team'
    teamm = TeamMember.objects.filter(member=user, team=team).first()
    if not teamm:
        return 'You are not in this team'
    teamm.delete()
    for docpower in DocPower.objects.filter(member=user, doc__team=team):
        docpower.delete()
    for doc in Doc.objects.filter(creator=user, team=team):
        doc.content.delete()
        doc.delete()
    msg = '您已经成功退出了"{0}"小队。期待您的再次加入(*^_^*)'.format(team.name)
    Message.objects.create(receiver=user, content=msg)
    msg = '队员{0}已经退出了您的’{1}‘小队，愿以后有缘再相聚＞﹏＜'.format(user.name, team.name)
    Message.objects.create(receiver=team.creator, content=msg)
    return 'true'

def getBasicInfo(teamid):
    team = Team.objects.filter(id = teamid).first()
    if not team:
        return 'Team inexisted'
    return team.name
