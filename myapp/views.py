from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from .forms import MessagesForm,CustomPasswordChangeForm,SearchForm
from .models import CustomUser,Messages
from django.contrib.auth import login , authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views import generic

class IndexView(generic.TemplateView):
    template_name = "myapp/index.html"



@login_required
def friends(request):
    if request.method == 'POST':
        self_pk = request.user.pk
        form = SearchForm(request.POST)
        if form.is_valid():
            self_pk = request.user.pk #自分自身を取得
            if form.cleaned_data["friend_name"]=="":
                data = CustomUser.objects.exclude(Q(pk = self_pk)|Q(username = "admin"))
                me = CustomUser.objects.filter(pk=self_pk)
                params = {
                    "data" : data,
                    "me"    : me,
                    'form' : form,
                }
                return render(request, "myapp/friends.html",params)   
            else:
                data = CustomUser.objects.filter(username = form.cleaned_data["friend_name"]).exclude(Q(pk = self_pk)|Q(username = "admin"))
                me = CustomUser.objects.filter(pk=self_pk)
                params = {
                    "data" : data,
                    "me"    : me,
                    'form' : form,
                }
                return render(request, "myapp/friends.html",params)
    else:
        form = SearchForm(request.POST)
        self_pk = request.user.pk #自分自身を取得
        data = CustomUser.objects.exclude(Q(pk = self_pk)|Q(username = "admin"))
        me = CustomUser.objects.filter(pk=self_pk)
        params = {
            "data" : data,
            "me"    : me,
            'form' : form,
        }
        return render(request, "myapp/friends.html",params)


# class FriendView(LoginRequiredMixin,generic.ListView):
#     template_name = "myapp/friends.html"
#     model = CustomUser
#     def get_context_data(self):
#         self_pk = self.request.user.pk #自分自身を取得
#         data = CustomUser.objects.exclude(Q(pk = self_pk)|Q(username = "admin"))
#         me = CustomUser.objects.filter(pk=self_pk)
#         params = {
#             "data" : data,
#             "me"    : me
#         }
#         return params

@login_required
def talk_room(request, pk):
    form = MessagesForm(request.POST)
    self_pk = request.user.pk
    self_name = request.user.username
    data = Messages.objects.filter(Q(message_to = pk , message_from = self_pk)|Q(message_to = self_pk,message_from = pk)) #getはひとつだけ!!
    tmp = CustomUser.objects.get(pk = pk)
    friend_name = tmp.username
    params = {
        "pk" : pk,
        "friend_name" : friend_name,
        "self_name" : self_name,
        "self_pk" : self_pk,
        'form' : form,
        "data" : data
    }
    return render(request, "myapp/talk_room.html",params)

def submit(request,pk):
    if request.method == 'POST':
        self_pk = request.user.pk
        form = MessagesForm(request.POST)
        if form.is_valid():
            Messages.objects.create(
                message_from = self_pk,
                message_to = pk,
                message = form.cleaned_data["message"]
            )
            return redirect('talk_room',pk)
    else:
        return redirect('talk_room',pk)


# class Talk_roomView(LoginRequiredMixin,generic.ListView):
#     template_name = "myapp/talk_room.html"
#     form_class = MessagesForm
#     model = Messages
#     def submit(request,pk):
#         if request.method == 'POST':
#             self_pk = request.user.pk
#             form = MessagesForm(request.POST)
#             if form.is_valid():
#                 Messages.objects.create(
#                     message_from = self_pk,
#                     message_to = pk,
#                     message = form.cleaned_data["message"]
#                 )
#                 return redirect('talk_room',pk)
#         else:
#             return redirect('talk_room',pk)
#     def get_context_data(self,request,pk):
#         form = MessagesForm(request.POST)
#         self_name = request.user.username
#         self_pk = request.user.pk
#         data = Messages.objects.filter(Q(message_to = pk , message_from = self_pk)|Q(message_to = self_pk,message_from = pk)) #getはひとつだけ!!
#         tmp = CustomUser.objects.get(pk = pk)
#         friend_name = tmp.username
#         params = {
#             "pk" : pk,
#             "friend_name" : friend_name,
#             "self_name" : self_name,
#             "self_pk" : self_pk,
#             'form' : form,
#             "data" : data
#         }
#         return params
    

# @login_required
# def setting(request):
#     return render(request, "myapp/setting.html")


class SettingView(LoginRequiredMixin,generic.TemplateView):
    template_name ="myapp/setting.html"


        

class Logout(LogoutView):
    template_name = 'myapp/logout.html'
    
def address_change(request):
    self_name = request.user.username
    if request.method == 'POST':
        new_email = request.POST.get("new_email")
        user = CustomUser.objects.get(username = self_name)
        user.email = new_email
        user.save()
        return redirect('setting')
    else:
        return render(request,"myapp/address_change.html")
    
class AddressChangeView(generic.UpdateView):
    template_name = "myapp/address_change.html"
    model = CustomUser

def username_change(request):
    self_name = request.user.username
    if request.method == 'POST':
        new_username = request.POST.get("new_username")
        user = CustomUser.objects.get(username = self_name)
        user.username = new_username
        user.save()
        return redirect('setting')
    else:
        return render(request,"myapp/username_change.html")

# class UsernameChangeView(generic.UpdateView):
#     template_name = "myapp/username_change.html"
#     model = CustomUser

def icon_change(request):
    self_name = request.user.username
    if request.method == 'POST':
        new_icon = request.FILES.get("new_icon")
        user = CustomUser.objects.get(username = self_name)
        user.file = new_icon
        user.save()
        return redirect('setting')
    else:
        return render(request,"myapp/icon_change.html")
    

# class IconChangeView(generic.UpdateView):
#     template_name = "myapp/icon_change.html"
#     model = CustomUser

class PasswordChange(PasswordChangeView):
    template_name = "myapp/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'myapp/password_change_done.html'