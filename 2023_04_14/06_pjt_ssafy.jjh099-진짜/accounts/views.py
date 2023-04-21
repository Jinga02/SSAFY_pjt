from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import  AuthenticationForm, UserCreationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash # 암호 변경시 세션 무효화 방지
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from movies.models import Movie
# require_http_methods(메소드)
# require_POST : POST만 허용 require_safe : GET만 허용

# Create your views here.
@require_http_methods(['POST','GET'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        print('확인')
        print(form)
        if form.is_valid():
            print('확인2')
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'movies/index.html', context)

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
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

@require_POST
def signout(request):
    if request.method == "POST":
        user = request.user # 현재 request의 user정보를 바로 받아올 수 있다.
        user.delete()
        auth_logout(request) # Session까지 제거
        return redirect('movies:index')
    else:
        return render(request, 'accounts/signout.html')
        

# @require_http_methods(['POST']) # POST만 접근 허용 
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

@require_safe
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    # movie = Movie.objects.get(username=username)
    context = {
        'person' : person,
        # 'movie' : movie
    }
    return render(request, 'accounts/profile.html', context)

@require_POST
def follow(request, pk):
    if request.user.is_authenticated:   # 로그인 되있으면
        person = get_user_model().objects.get(pk=pk)
        if person != request.user:  # 로그인한 유저와 보고 있는 유저가 다르면
            if person.followers.filter(pk=request.user.pk).exists():
                person.followers.remove(request.user)
            else:
                person.followers.add(request.user)
        return redirect('accounts:profile', person.username)
    return redirect('accounts:login')

