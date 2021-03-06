"""generate database test data"""
import random
import string
from django.core import signing

from .models import User, DocContent, Doc, DocTemplate, Browse, Favorite, Team
from .models import TeamMember, DocPower, Comment, Message


# random.seed(1000)

def rand_str(num):
    num = min(num, 60)
    num = random.randint(5, num)
    return ''.join(random.sample(string.ascii_letters + string.digits, num))

def add_data():
    add_user()
    add_doc()
    add_doc_template()
    add_browse()
    add_favorite()
    add_team()
    add_team_member()
    add_doc_power()
    add_comment()
    add_message()


def add_user():
    users = []
    for _ in range(20):
        users.append(User(name=rand_str(10), password=random.randint(100000, 999999)))

    User.objects.bulk_create(users)
    print('Users add finished')

def add_doc():
    docs = []
    # doccs=[]
    for _ in range(20):
        dcc = DocContent(title=rand_str(10), content=rand_str(100))
        dcc.save()
        creator = User.objects.order_by('?')[:2].first()
        doc = Doc(creator=creator, content=dcc)
        docs.append(doc)
        # doccs.append(dcc)

    Doc.objects.bulk_create(docs)
    # Doc_content.objects.bulk_create(doccs)
    print('Docs add finished')

def add_doc_template():
    docts = []
    # doccs = []
    for _ in range(10):
        dcc = DocContent(title=rand_str(10), content=rand_str(100))
        dcc.save()
        dct = DocTemplate(content=dcc, name=rand_str(10))
        docts.append(dct)
        # doccs.append(dcc)

    DocTemplate.objects.bulk_create(docts)
    # Doc_content.objects.bulk_create(doccs)
    print('Doc_templates add finished')

def add_browse():
    browses = []
    for _ in range(10):
        uid = User.objects.order_by('?')[:2].first()
        did = Doc.objects.order_by('?')[:2].first()
        browses.append(Browse(uid=uid, did=did))
    Browse.objects.bulk_create(browses)
    print('Browse add finished')

def add_favorite():
    favorites = []
    for _ in range(10):
        uid = User.objects.order_by('?')[:2].first()
        did = Doc.objects.order_by('?')[:2].first()
        favorites.append(Browse(uid=uid, did=did))
    Favorite.objects.bulk_create(favorites)
    print('Favorites add finished')

def add_team():
    teams = []
    for _ in range(5):
        name = rand_str(10)
        creator = User.objects.order_by('?')[:2].first()
        teams.append(Team(name=name, creator=creator))
    Team.objects.bulk_create(teams)
    print('Teams add finished')


def add_team_member():
    team_members = []
    users = User.objects.order_by('?')
    num = len(users)
    for user in users[:int(num/2)]:
        team = Team.objects.order_by('?')[:2].first()
        team_members.append(TeamMember(team=team, member=user))
        team.member_num += 1
    for user in users[int(num/2):int(num*2/3)]:
        team = Team.objects.order_by('?')[:2]
        team_members.append(TeamMember(team=team[0], member=user))
        team_members.append(TeamMember(team=team[0], member=user))
        team[0].member_num += 1
        team[1].member_num += 1
    TeamMember.objects.bulk_create(team_members)
    print('TeamMembers add finished')

def add_doc_power():
    doc_powers = []
    for doc in Doc.objects.all():
        doc_powers.append(DocPower(member=doc.creator, doc=doc, role=5))
    DocPower.objects.bulk_create(doc_powers)
    print('DocPowers add finished')

def add_comment():
    comments = []
    for doc in Doc.objects.order_by('?')[:10]:
        creator = User.objects.order_by('?')[:2].first()
        comments.append(Comment(creator=creator, doc=doc, content=rand_str(100)))
    Comment.objects.bulk_create(comments)
    print('Comments add finished')

def add_message():
    messages = []
    for user in User.objects.order_by('?')[:10]:
        messages.append(Message(receiver=user, content=rand_str(100)))
    Message.objects.bulk_create(messages)
    print('Messages add finished')


def my_test():
    print(User.objects.order_by('?')[:2].first())

def encrypt(src):
    """encoding"""
    print(src)
    value = signing.dumps(src)
    print(value)
    return value

def decrypt(value):
    """decoding"""
    print(value)
    src = signing.loads(value)
    print(src)
    return src
