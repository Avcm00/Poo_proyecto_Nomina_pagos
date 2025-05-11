from django.shortcuts import render, redirect, get_object_or_404,HttpResponse

def login(request):
  return render(request, "login/login.html")

def index(request):
  return render(request, "index.html")