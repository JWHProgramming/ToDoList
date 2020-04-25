from django.shortcuts import render, HttpResponse, redirect

def index(request):
    return render(request, "list_app/index.html")

def home(request):
    return render(request, "list_app/home.html")

def signup(request):
    pass
