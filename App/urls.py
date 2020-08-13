from django.urls import path
from App import views

app_name = 'APP'

urlpatterns = [
    path('add_data/', views.add_data, name='add_data'),
    path('passport/login/', views.login, name='login'),
    path('passport/register/', views.register, name='register'),
    path('passport/check/', views.check, name='check'),
    path('doc/deletedoc/', views.deletedoc, name='deletedoc'),
    path('doc/recoverdoc/', views.recoverdoc, name='recoverdoc'),
    path('doc/deletedocconfirm/', views.deletedocconfirm, name='deletedocconfirm'),
    # path('my_test/', views.my_test, name='my_test'),
]