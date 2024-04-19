from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash

@require_http_methods(["GET","POST"])
def login(request) :
    if request.method == 'POST' :
        form = AuthenticationForm(data = request.POST)
        if form.is_valid() :
            auth_login(request,form.get_user())
            next_path = request.GET.get("next") or "products:list"
            return redirect(next_path)
    else :
        form = AuthenticationForm()

    return render(request, "accounts/login.html",{'form' : form})

@require_POST
def logout(request) :
    if request.user.is_authenticated :
        auth_logout(request)
    return redirect("products:list")

@require_http_methods(["GET","POST"])
def signup(request) :
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid() :
            user = form.save()
            auth_login(request, user)
            return redirect("products:list")
    else :
        form = UserCreationForm()
    return render(request,"accounts/signup.html",{'form':form})

@require_POST
def delete(request) :
    if request.user.is_authenticated :
        request.user.delete() # 탈퇴하기
        auth_logout(request) # 세션 지우기
    return redirect("products:list")

@require_http_methods({"GET","POST"})
def update(request) :
    if request.method == 'POST' :
        form = CustomUserChangeForm(request.POST,instance = request.user)
        if form.is_valid() :
            form.save()
            return redirect("products:list")
    else:        
        form = CustomUserChangeForm(instance = request.user)
    return render(request,"accounts/update.html",{'form':form})

@login_required
@require_http_methods(["GET","POST"])
def password(request) :
    if request.method == 'POST' :
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() :
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("products:list")
    else:
        form = PasswordChangeForm(request.user)
    return render(request,"accounts/password.html",{'form':form})
