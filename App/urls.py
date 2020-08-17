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
    path('userinfo/changeavatar/', views.change_avatar, name='change_avatar'),
    path('userinfo/getteam/', views.getteam, name = 'getteam'),


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
    path('doc/favorites/file/', views.doc_favorites_file, name = 'doc_favorites_file'),
    path('doc/used/file/', views.doc_used_file, name = 'doc_used_file'),
    path('doc/favordoc/', views.favordoc, name='favordoc'),
    path('doc/unfavordoc/', views.unfavordoc, name='unfavordoc'),
    path('doc/sharetoteam/', views.sharetoteam, name='sharetoteam'),
    path('doc/get-power/', views.get_power, name='get_power'),
    path('doc/get-corporation/', views.get_corporation, name = 'get_corporation'),
    path('doc/set-share-option/', views.set_share_option, name = 'set_share_option'),
    path('doc/set-power/', views.set_power, name = 'set_power'),


    #doc-system
    path('doc/desktop/file/', views.doc_desktop_file, name = 'doc_desktop_file'),
    path('doc/desktop/folder/', views.doc_desktop_folder, name = 'doc_desktop_folder'),
    path('doc/space/file/', views.doc_space_file, name = 'doc_space_file'),
    path('doc/space/folder/', views.doc_space_folder, name = 'doc_space_folder'),
    path('doc/folder/file/', views.doc_folder_file, name = 'doc_folder_file'),
    path('doc/folder/folder/', views.doc_folder_folder, name = 'doc_folder_folder'),


    #team
    path('team/create/', views.team_create, name = 'team_create'),
    path('team/disband/', views.team_disband, name = 'team_disband'),
    path('team/getlist/', views.team_getlist, name = 'team_getlist'),
    path('team/getinfo/', views.get_team_info, name='get_team_info'),
    path('team/invite/', views.invite, name='invite'),
    path('team/dealinginvite/', views.deal_invitation, name='deal_invitation'),
    path('team/removeuser/', views.remove_user, name='remove_user'),


    #user
    path('user/getlistbyname/', views.get_user_by_uname, name='get_user_by_uname'),


    # template
    path('template/getall/', views.get_template, name='get_template'),


    # comment
    path('comment/new/', views.new_comment, name='new_comment'),
    path('comment/get/', views.get_comment, name='get_comment'),
    path('comment/replyto/', views.reply, name='reply'),
    path('comment/delete/', views.delete_comment, name='delete_comment'),


    #messgae
    path('message/unreadnum/', views.get_unread_number, name='get_unread_number'),


    # etc
    path('add_data/', views.add_data, name='add_data'),
    path('my_test/', views.my_test, name='my_test'),
]