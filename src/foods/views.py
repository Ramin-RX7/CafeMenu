from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Category,Food

# Create your views here.

def category_list(request):
    plural = Category.objects.all()
    return render(request,'foods/category_list.html',{"plural":plural})

def food_details(request, pk):
    food = Food.objects.get(id=pk)
    return render(request, "food/food_details.html", {"food": food})

def search(request):
    if request.method != "GET":
        raise Http404
    return render(request,'foods/search.html')
