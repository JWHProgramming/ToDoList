from django.shortcuts import render, HttpResponse, render

def index(request):
    return render(request, "list_app/index.html")

def first(request):
    return HttpResponse("First page here")
