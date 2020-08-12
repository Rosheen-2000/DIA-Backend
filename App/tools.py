import random, string
from .models import User, DocContent, Doc, DocTemplate, Browse, Favorite, Team
from .models import TeamMember, DocPower, Comment, Message
from django.core import signing


# random.seed(1000)

def rand_str(num):
    num = min(num, 60)
    num = random.randint(5, num)
    return ''.join(random.sample(string.ascii_letters + string.digits, num))

def add_data():
    add_User()
    add_Doc()
    add_Doc_template()
    add_Browse()
    add_Favorite()
    add_Team()
    add_TeamMember()
    add_DocPower()
    add_Comment()
    add_Message()


def add_User():
    users=[]
    for i in range(20):
        users.append(User(name=rand_str(10), password=random.randint(100000,999999)))

    User.objects.bulk_create(users)
    print('Users add finished')

def add_Doc():
    docs=[]
    # doccs=[]
    for i in range(20):
        dcc = DocContent(title=rand_str(10), content=rand_str(100))
        dcc.save()
        du = User.objects.order_by('?')[:2].first()
        dc = Doc(creator=du, content=dcc)
        docs.append(dc)
        # doccs.append(dcc)

    Doc.objects.bulk_create(docs)
    # Doc_content.objects.bulk_create(doccs)
    print('Docs add finished')

def add_Doc_template():
    docts = []
    # doccs = []
    for i in range(10):
        dcc = DocContent(title=rand_str(10),
                          content=rand_str(100))
        dcc.save()
        dct = DocTemplate(content=dcc, name=rand_str(10))
        docts.append(dct)
        # doccs.append(dcc)

    DocTemplate.objects.bulk_create(docts)
    # Doc_content.objects.bulk_create(doccs)
    print('Doc_templates add finished')

def add_Browse():
    browses=[]
    for i in range(10):
        bu = User.objects.order_by('?')[:2].first()
        du = Doc.objects.order_by('?')[:2].first()
        browses.append(Browse(uid=bu, did=du))
    Browse.objects.bulk_create(browses)
    print('Browse add finished')

def add_Favorite():
    favorites=[]
    for i in range(10):
        bu = User.objects.order_by('?')[:2].first()
        du = Doc.objects.order_by('?')[:2].first()
        favorites.append(Browse(uid=bu, did=du))
    Favorite.objects.bulk_create(favorites)
    print('Favorites add finished')

def add_Team():
    teams = []
    for i in range(5):
        name = rand_str(10)
        creator = User.objects.order_by('?')[:2].first()
        teams.append(Team(name = name, creator = creator))
    Team.objects.bulk_create(teams)
    print('Teams add finished')


def add_TeamMember():
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

def add_DocPower():
    doc_powers = []
    for doc in Doc.objects.all():
        doc_powers.append(DocPower(member = doc.creator, doc = doc, role = 5))
    DocPower.objects.bulk_create(doc_powers)
    print('DocPowers add finished')
 
def add_Comment():
    comments = []
    for doc in Doc.objects.order_by('?')[:10]:
        creator=User.objects.order_by('?')[:2].first()
        comments.append(Comment(creator=creator, doc=doc, content=rand_str(100)))
    Comment.objects.bulk_create(comments)
    print('Comments add finished')
    

def add_Message():
    messages = []
    for user in User.objects.order_by('?')[:10]:
        messages.append(Message(receiver=user, content=rand_str(100)))
    Message.objects.bulk_create(messages)
    print('Messages add finished')


def my_test():
    print(User.objects.order_by('?')[:2].first())

def encrypt(src):
    print(src)
    value = signing.dumps(src)
    print(value)
    return value

def decrypt(value):
    print(value)
    src = signing.loads(value)
    print(src)
    return src

