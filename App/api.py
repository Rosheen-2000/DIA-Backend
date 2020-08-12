from .models import User, Doc, DocPower, DocContent, DocTemplate, Browse, Team, TeamMember, Favorite, Comment, Message
from . import tools

def login(name, password):
	print(name, password)
	user = User.objects.filter(name=name).first()
	print(user)
	if user is not None:
		if user.password == password:
			value = tools.encrypt(user.password)
			return True, value

	return False, ""
