from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/user_<id>/<filename>
    return 'avatar/user_{0}/{1}'.format(instance.id, filename)

class User(models.Model):
    # uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    tel = models.CharField(max_length=200, unique=True, null=True)
    mail = models.CharField(max_length=200, unique=True, null=True)
    description = models.CharField(max_length=200, null=True)
    avatar = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'User'

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    member_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Team'


class Folder(models.Model):
    # fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    father = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folder')
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now_add=True)
    isdeleted = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='folder', null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Folder'


class DocContent(models.Model):
    # did = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Doc_content'


def doc_template_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/template_pic/tem_<id>/<filename>
    return 'template_pic/tem_{0}/{1}'.format(instance.id, filename)

class DocTemplate(models.Model):
    # tid = models.AutoField(primary_key=True)
    content = models.OneToOneField(DocContent, on_delete=models.CASCADE, related_name='temp_header')
    # name = models.CharField(max_length=200, unique=True)
    picture = models.ImageField(upload_to=doc_template_directory_path, null=True, blank=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.content.title

    class Meta:
        db_table = 'Doc_template'


class Doc(models.Model):
    # did = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.OneToOneField(DocContent, on_delete=models.CASCADE, related_name='doc_header', default="")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='docs')
    isdeleted = models.IntegerField(default=0)
    modify_time = models.DateTimeField(auto_now_add=True)
    modify_num = models.IntegerField(default=0)
    modify_people = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='docs')
    father = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='doc', null=True)
    edit_status = models.IntegerField(default=0)
    type = models.IntegerField(default=0)

    def __str__(self):
        return self.content.title

    class Meta:
        db_table = 'Doc'


class DocStatus(models.Model):
    # did = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doc_status')
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='doc_status')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Doc_status'


class Browse(models.Model): 
    # bid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='browse', default="")
    did = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='browse', default="")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Browse'


class Favorite(models.Model):
    # fid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite', default="")
    did = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='favorite', default="")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Favorite'


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_member')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_member')
    join_time = models.DateTimeField(auto_now_add=True)
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
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now_add=True)
    star = models.IntegerField(default=0)
    quote = models.ForeignKey('self', on_delete=models.CASCADE, related_name='isquoted', null=True)

    def __str__(self):
        return self.creator.name + '_' + self.doc.__str__()

    class Meta:
        db_table = 'Comment'


class LikeRecord(models.Model):
    # lid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_record')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='like_record')

    class Meta:
        db_table = 'Like_record'


class Message(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message')
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200)
    mode = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, null=True)
    is_send = models.IntegerField(default=0)

    def __str__(self):
        return 'to' + self.receiver.name 

    class Meta:
        db_table = 'Message'
        