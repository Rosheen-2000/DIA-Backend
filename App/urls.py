from django.urls import path
from App import views

app_name = 'APP'

urlpatterns = [
    path('add_data/', views.add_data, name='add_data'),
    path('passport/login/', views.login, name='login'),
    path('passport/register/', views.register, name='register'),
    path('passport/check/', views.check, name='check'),
    path('doc/newdoc', views.new_doc, name='new_doc'),
    path('doc/modifydoccontent', views.modify_doc_content, name='modify_doc_content')
]
