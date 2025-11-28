from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    if request.method == 'post':
            username = request.post['username']
            password = request.post['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                 login(request, user)
                 messages.success(request, "LogIn successful!")
                 return redirect('home')
            else:
                 messages.error(request, "Something went wrong, try again")
                 redirect('home')

    else:
        return render(request, 'website/home.html', {})


def logout_user(request):
    pass