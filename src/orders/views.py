from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def order_list(request):
    return HttpResponse("hello world")

def order_details(request):
    return HttpResponse("hello world")