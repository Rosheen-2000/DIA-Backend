from django.urls import path
from App import views

app_name = 'APP'

urlpatterns = [
    # passport
    path('passport/login/', views.login, name='login'),
    path('passport/register/', views.register, name='register'),
    path('passport/check/', views.check, name='check'),

    # userinfo
    path('userinfo/changename/', views.modify_uname, name='changename'),
    path('userinfo/changepwd/', views.modify_pwd, name='changepwd'),
    path('userinfo/changemail/', views.changemail, name = 'changemail'),
    path('userinfo/changephoneno/', views.changephoneno, name = 'changephoneno'),
    path('userinfo/basic/', views.userinfo_basic, name='userinfo_basic'),
    path('userinfo/all/', views.userinfo_all, name='userinfo_all'),

    # doc
    path('doc/deletedoc/', views.deletedoc, name='deletedoc'),
    path('doc/recoverdoc/', views.recoverdoc, name='recoverdoc'),
    path('doc/deletedocconfirm/', views.deletedocconfirm, name='deletedocconfirm'),
    path('doc/newdoc/', views.new_doc, name='new_doc'),
    path('doc/modifydoccontent/', views.modify_doc_content, name='modify_doc_content'),
    path('doc/modifydoctitle/', views.modifydoctitle, name='modifydoctitle'),
    path('doc/getdoccontent/', views.getdoccontent, name='getdoccontent'),
    path('doc/own/file/', views.doc_own_file, name='doc_own_file'),
    path('doc/trash/file/', views.doc_trash_file, name='doc_trash_file'),

    # template
    path('template/getall/', views.get_template, name='get_template'),

    # etc
    path('add_data/', views.add_data, name='add_data'),
    path('my_test/', views.my_test, name='my_test')
]