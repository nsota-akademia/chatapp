from django.shortcuts import redirect, render
from .forms import SignUpForm,LoginForm,MessagesForm
from .models import CustomUser,Messages
from django.contrib.auth import login , authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.views import LogoutView

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = SignUpForm(request.POST,request.FILES)
    return render(request, "myapp/signup.html",{'form' : form})

def login_view(request):
    form = LoginForm(request.POST)
    return render(request, "myapp/login.html",{'form' : form})

@login_required
def friends(request):
    self_name = request.user.username #自分自身を取得
    data = CustomUser.objects.exclude(Q(username = self_name)|Q(username = "admin"))
    params = {
        "data" : data
    }
    return render(request, "myapp/friends.html",params)

@login_required
def talk_room(request, friend_name):
    form = MessagesForm(request.POST)
    self_name = request.user.username
    data = Messages.objects.filter(Q(message_to = friend_name , message_from = self_name)|Q(message_to = self_name,message_from = friend_name)) #getはひとつだけ!!
    params = {
        "friend_name" : friend_name,
        "self_name" : self_name,
        'form' : form,
        "data" : data
    }
    return render(request, "myapp/talk_room.html",params)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")


def usercreate(request):
    if request.method == 'POST':
        # フォーム送信データを受け取る
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
            # バリデーションを通過したデータは form.cleaned_data['<フィールド名>'] で取得
            # バリデーションを通過したデータをセットして create
        else:
            return redirect('signup_view')              
 
    else:
        form = SignUpForm()
        return redirect('signup_view')

def loginprocess(request):
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
            return redirect('login_view')
    else:
        form = LoginForm()
        
def submit(request,friend_name):
    if request.method == 'POST':
        self_name = request.user.username
        form = MessagesForm(request.POST)
        if form.is_valid():
            Messages.objects.create(
                message_from = self_name,
                message_to = friend_name,
                message = form.cleaned_data["message"]
            )
            return redirect('talk_room',friend_name)
    else:
        return redirect('talk_room')

class Logout(LogoutView):
    template_name = 'myapp/logout.html'
    
def username_change(request):
    pass
def address_change(request):
    pass
def icon_change(request):
    pass
def password_change(request):
    pass
