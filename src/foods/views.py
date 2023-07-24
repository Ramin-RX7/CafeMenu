from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def category_list(request):
    return HttpResponse("Hello World")

def food_details(request):
    return HttpResponse("Hello world")