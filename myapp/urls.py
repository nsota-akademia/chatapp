from django.urls import path
from . import views
from .views import Logout

urlpatterns = [
    path('', views.index, name='index'),
    path('signup_view', views.signup_view, name='signup_view'),
    path('login_view',views.login_view,name="login_view"),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>', views.talk_room, name='talk_room'),
    path('submit/<int:pk>',views.submit,name="submit"),
    path('setting', views.setting, name='setting'),
    path('setting/username_change',views.username_change,name="username_change"),
    path('setting/address_change',views.address_change,name="address_change"),
    path('setting/icon_change',views.icon_change,name="icon_change"),
    path('setting/password_change', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('logout',Logout.as_view(),name="logout"),
]
