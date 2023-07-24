from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def category_list(request):
    return HttpResponse("hello world")

def food_details(request):
    return HttpResponse("hello world")