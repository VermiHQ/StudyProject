from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user


# Create our views
@unauthenticated_user
def register_page(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан для ' + form.cleaned_data.get('username'))
            return redirect('auth:login')
        else:
            s = ''
            for key in form.error_messages:
                s += str(form.error_messages[key])
            messages.error(request, 'Ошибка при регистрации! ' + s)
    else:
        form = CreateUserForm
    context = {
        'form': form
    }
    return render(request, 'authentification/reg.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dish:index')
        else:
            messages.warning(request, 'Имя пользователя и пароль не совпадают!')
    return render(request, 'authentification/login.html')

def logout_page(request):
    logout(request)
    return redirect('auth:login')
