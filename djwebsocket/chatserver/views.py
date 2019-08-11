from django.shortcuts import render, redirect
from .forms import UserLoginForm, CreateUserForm, authenticate, User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

def login(request):
    form = UserLoginForm(request.POST or None)
    if request.user.is_authenticated:
        return render(request, 'chatserver/index.html')

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        # else:
        #     return error_response_render(request, 'memo/login.html', {'form': form, 'error': '로그인 실패!'})
    else:
        try:
            username = form.cleaned_data.get('username')
            existsUser = User.objects.filter(username=username).exists()

            # if existsUser is False:
            #     return error_response_render(request, 'memo/login.html', {'form': form, 'error': '가입되지 않은 회원입니다!'})
        except:
            return render(request, 'chatserver/login.html', {'form': form})

    return render(request, 'chatserver/login.html')

def signup(request):
    form = CreateUserForm(request.POST or None) #회원가입 폼

    if request.user.is_authenticated:
        return redirect('index')

    if form.is_valid():
        username = form.cleaned_data['username'] #유저 E-mail
        password = form.cleaned_data['password1']
        retype_password = form.cleaned_data['password2']

        password_valid = password == retype_password
        existsUser = User.objects.filter(username=username).exists()

        # if password_valid is False:
        #     return error_response_render(request, 'memo/signup.html', {'form': form, 'error': '비밀번호 확인을 해주세요.'})
        #
        # if existsUser is True:
        #     return error_response_render(request, 'memo/signup.html', {'form': form, 'error': '이미 가입된 회원입니다.'})
        user = form.signup()
        auth_login(request, user)
        return render(request, 'chatserver/index.html')

    return render(request, 'chatserver/signup.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'chatserver/index.html', {})

def test(request):
    return render(request, 'chatserver/test.html', {})