from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import  AuthenticationForm, UserCreationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash # 암호 변경시 세션 무효화 방지

from django.views.decorators.http import require_http_methods, require_POST, require_safe
# require_http_methods(메소드)
# require_POST : POST만 허용 require_safe : GET만 허용

# Create your views here.
@require_http_methods(['POST','GET'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)

@require_http_methods(['POST','GET'])
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['POST','GET'])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request.user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

def signout(request):
    if request.method == "POST":
        user = request.user # 현재 request의 user정보를 바로 받아올 수 있다.
        user.delete()
        auth_logout(request) # Session까지 제거
        return redirect('movies:index')
    else:
        return render(request, 'accounts/signout.html')
        

# @require_http_methods(['POSt']) # POST만 접근 허용 
# @require_POST   # POST만 접근 허용 둘 중 하나 사용하면 됨.
def delete(request):
    user = request.user # 현재 request의 user정보를 바로 받아올 수 있다.
    user.delete()
    auth_logout(request) # Session까지 제거
    return redirect('movies:index')

@require_http_methods(['POST','GET'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context={
        'form':form
    }
    return render(request, 'accounts/update.html', context)


@require_http_methods(['POST','GET'])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 암호가 변경되어도 로그아웃 되지 않도록 새로운 암호의 session data로 업데이트
            update_session_auth_hash(request, form.user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context={
        'form':form
    }
    return render(request, 'accounts/password.html', context)

