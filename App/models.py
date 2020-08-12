from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, null=False)
    password = models.CharField(max_length=200, null=False)
    tel = models.CharField(max_length=200, unique=True, null=True)
    mail = models.CharField(max_length=200, unique=True, null=True)
    description = models.CharField(max_length=200, null=True)
    profile = models.ImageField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'User'


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    member_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Team'



class DocContent(models.Model):
    did = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Doc_content'


class DocTemplate(models.Model):
    tid = models.AutoField(primary_key=True)
    content = models.OneToOneField(DocContent, on_delete=models.CASCADE, related_name='temp_header')
    name = models.CharField(max_length=200, unique=True)
    picture = models.ImageField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Doc_template'


class Doc(models.Model):
    did = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    create_time = models.DateTimeField(auto_now=True)
    content = models.OneToOneField(DocContent, on_delete=models.CASCADE, related_name='doc_header', default="")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='docs')
    isdeleted = models.IntegerField(default=0)
    modify_time = models.DateTimeField(auto_now_add=True)
    modify_num = models.IntegerField(default=0)
    modify_people = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='docs')

    def __str__(self):
        return self.content.title

    class Meta:
        db_table = 'Doc'


class Browse(models.Model): 
    bid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='browses', default="")
    did = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='browses', default="")
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Browse'


class Favorite(models.Model):
    fid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', default="")
    did = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='favorites', default="")
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Favorite'


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_member')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_member')
    join_time = models.DateTimeField(auto_now=True)
    role = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name + '_' + self.member.name

    class Meta:
        db_table = 'TeamMember'


class DocPower(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='DocPower')
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='DocPower')
    role = models.IntegerField(default=0)
    is_commented = models.BooleanField(default=False)

    def __str__(self):
        return self.member.name + '_' + self.doc.__str__()

    class Meta:
        db_table = 'DocPower'


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='comment')
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now=True)
    modify_time = models.DateTimeField(auto_now=True)
    star = models.IntegerField(default=0)

    def __str__(self):
        return self.creator.name + '_' + self.doc.__str__()

    class Meta:
        db_table = 'Comment'


class Message(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=500)
    mode = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'to' + self.receiver.name 

    class Meta:
        db_table = 'Message'
        