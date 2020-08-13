from django.urls import path
from App import views

app_name = 'APP'

urlpatterns = [
    path('add_data/', views.add_data, name='add_data'),
    path('password/login/', views.login, name='login'),
    path('password/register/', views.register, name='register'),
    path('password/check/', views.register, name='check'),

]