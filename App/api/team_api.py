import datetime

from django.utils import timezone

from ..models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message, Folder, LikeRecord, DocStatus
from ..tools import encrypt, decrypt, updateBrowse


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
    members = []
    for member in TeamMember.objects.filter(team=team):
        if member.member is None:
            continue
        members.append({'uid':str(member.member.id), 'uname':member.member.name,
                        'useravatar':member.member.avatar.url if member.member.avatar else ''})
    return team.name, team.creator.name, team.creator.avatar.url if team.creator.avatar else '', \
           team.create_time, members

def get_user_by_uname(uname):
    user = User.objects.filter(name=uname).first()
    if not user:
        return '', '', ''
    return user.name, user.avatar.url if user.avatar else '', user.id

def invite(user, teamid, uid):
    team = Team.objects.filter(id=teamid).first()
    if not team:
        return 'Team does not exist.'
    invitee = User.objects.filter(id=uid).first()
    if not invitee:
        return 'The invitee does not exist.'
    if user != team.creator: # 暂定仅队长有权邀请新成员
        return 'No permission to invite.'
    team_member = TeamMember.objects.filter(team=team, member=invitee).first()
    if team_member:
        return 'This person is already in the team'
    content = 'from team {0}'.format(team.name) # 邀请消息文本格式？
    Message.objects.create(team=team, content=content, receiver=invitee, mode=1)
    return 'true'

