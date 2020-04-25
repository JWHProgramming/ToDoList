from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, "list_app/index.html")

def home(request):
    pass

def register(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password
        )
        request.session["user_id"] = user.id
        messages.success(request, "Successfully registered!")
        return redirect("/user")