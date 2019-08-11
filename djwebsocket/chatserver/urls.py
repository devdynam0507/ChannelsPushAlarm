from django.urls import path
from . import views, channels_api

urlpatterns = [
    path('', views.index, name='index'),
    path('api/send_push_user', channels_api.send_user_push_alarm),
    path('api/send_push_admin', channels_api.send_admin_push_alarm),
    path('signin/', views.login),
    path('signup/', views.signup),
    path('logout/', views.logout_request)
]