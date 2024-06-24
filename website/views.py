from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    # Check to see if loggin in
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error loggin in, please try again.")
            return redirect('home')

    return render(request, 'home.html', {})

def login_user(request):
    pass

def logout_user(request):
    pass

