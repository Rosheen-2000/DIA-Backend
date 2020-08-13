from .models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message
from .tools import encrypt, decrypt

def login(name, password):
    user = User.objects.filter(name=name).first()
    if user:
        if user.password == password:
            value = encrypt(user.password)
            return True, value
        return "Wrong Password", ''

    return "Username does not exist.", ''

def register(name, password):
    if check(name) != True:
        return "Username exists.", ''
    User.objects.create(name=name, password=password)
    return True, encrypt(password)

def check(name):
    if User.objects.filter(name=name).first():
        return "Username exists."
    return True
