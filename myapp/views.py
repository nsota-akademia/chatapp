from django.shortcuts import redirect, render
from .forms import SignUpForm,LoginForm,MessagesForm,PasswordForm
from .models import CustomUser,Messages
from django.contrib.auth import login , authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView
from django.urls import reverse_lazy

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        # フォーム送信データを受け取る
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
            # バリデーションを通過したデータは form.cleaned_data['<フィールド名>'] で取得
            # バリデーションを通過したデータをセットして create
        else:
            return render(request, "myapp/signup.html",{'form' : form})              
    else:
        form = SignUpForm(request.POST,request.FILES)
        return render(request, "myapp/signup.html",{'form' : form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            name = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username = name , password = password)
            if user is not None:
                login(request,user)
                return redirect('friends')
        else:
            return render(request, "myapp/login.html",{'form' : form})
    else:
        form = LoginForm(request.POST)
        return render(request, "myapp/login.html",{'form' : form})

@login_required
def friends(request):
    self_pk = request.user.pk #自分自身を取得
    data = CustomUser.objects.exclude(Q(pk = self_pk)|Q(username = "admin"))
    params = {
        "data" : data
    }
    return render(request, "myapp/friends.html",params)

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

@login_required
def setting(request):
    return render(request, "myapp/setting.html")



        
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

class PasswordChange(PasswordChangeView):
    template_name = "myapp/password_change.html"
    form_class = PasswordForm
    success_url = reverse_lazy('password_change_done')

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'myapp/password_change_done.html'
