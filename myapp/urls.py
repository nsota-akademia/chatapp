from django.urls import path
from . import views
from .views import Logout

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('friends/',views.FriendView.as_view(),name="friends"),
    # path('talk_room/<int:pk>', views.Talk_roomView.as_view(), name='talk_room'),
    path('setting', views.SettingView.as_view(), name='setting'),
    # path('setting/username_change',views.UsernameChangeView.as_view(),name="username_change"),
    # path('setting/address_change',views.AddressChangeView.as_view(),name="address_change"),
    # path('setting/icon_change',views.IconChangeView.as_view(),name="icon_change"),
    path('setting/password_change', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('logout',Logout.as_view(),name="logout"),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>', views.talk_room, name='talk_room'),
    path('submit/<int:pk>',views.submit,name="submit"),
    # path('submit/<search>',views.submit,name="submit"),
    # path('setting', views.setting, name='setting'),
    path('setting/username_change',views.username_change,name="username_change"),
    path('setting/address_change',views.address_change,name="address_change"),
    path('setting/icon_change',views.icon_change,name="icon_change"),
    
]
