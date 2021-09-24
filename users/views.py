from django.shortcuts import render
from users.forms import userLoginForm


def login(request):
    form = userLoginForm()
    context = {
        'title': 'Geekshop - Авторизация',
        'form': form,
    }
    return render(request,'users/login.html',context)

def register(request):
    context = {
        'title': 'Geekshop - Регистрация',
    }
    return render(request,'users/register.html',context)