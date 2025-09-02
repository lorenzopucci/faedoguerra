from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def auth_login(request):
    if request.method == 'GET':
        return render(request, 'auth/login.jinja')

    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST["username"],
            password = request.POST["password"]
        )

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'auth/login.jinja', {
                'wrong_credentials': True
            })
