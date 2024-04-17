from django.shortcuts import render,redirect

def index(request) :
    return render(request,"products/index.html")

def detail(request) :
    return render(request,"products/detail.html")

def create(request) :
    return render(request,"products/create.html")

