from django.urls import path
from . import views
from .views import Logout

urlpatterns = [
    path('', views.index, name='index'),
    path('signup_view', views.signup_view, name='signup_view'),
    path('login_view', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<friend_name>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('usercreate',views.usercreate,name='usercreate'),
    path('login',views.loginprocess,name="login"),
    path('submit/<friend_name>',views.submit,name="submit"),
    path('logout',Logout.as_view(),name="logout"),
    path('setting/username_change',views.username_change,name="username_change"),
    path('setting/address_change',views.address_change,name="address_change"),
    path('setting/icon_change',views.icon_change,name="icon_change"),
    path('setting/password_change',views.password_change,name="password_change"),
]
