from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, "list_app/index.html")

def home(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["user_id"])
        context = {
            "user" : user,
            "items" : user.items.all().order_by("created_at")
        }
        return render(request, "list_app/home.html", context)

def register(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"].lower()
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password.decode()
        )
        request.session["user_id"] = user.id
        messages.success(request, "Successfully registered!")
        return redirect("/home")

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("/")
    else:
        user = User.objects.get(email=request.POST["login_email"].lower())
        request.session["user_id"] = user.id
        return redirect("/home")

def logout(request):
    if "user_id" in request.session:
        request.session.clear()
    return redirect("/")

def add(request):
    errors = Item.objects.item_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("/home")
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        user = User.objects.get(id=request.session["user_id"])
        Item.objects.create(
            title = title,
            description = description,
            user = user
        )
        return redirect("/home")

def complete_toggle(request, id):
    new_id = int(id)
    item = Item.objects.get(id=new_id)

    item.is_complete=True
    item.save()
    return redirect("/home")

def reorder(request, val):
        new_val = int(val)
        user = User.objects.get(id=request.session["user_id"])

        context = {
            "user" : user
        }

        if new_val == 1:
            context["items"] = user.items.all().order_by("-created_at")
            return render(request, "list_app/home.html", context)
        elif new_val == 2:
            context["items"] = user.items.all().order_by("created_at")
            return render(request, "list_app/home.html", context)
        elif new_val == 3:
            context["items"] = user.items.all().order_by("title")
            return render(request, "list_app/home.html", context)
        else:
            context["items"] = user.items.all()
            return render(request, "list_app/home.html", context)
    