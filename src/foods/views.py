from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.

def category_list(request):
    return HttpResponse("hello world")

def food_details(request):
    return HttpResponse("hello world")

def search(request):
    if request.method != "GET":
        raise Http404
    return render(request,'foods/search.html')
