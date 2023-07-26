from django.shortcuts import render
from django.http import HttpResponse
from .models import Category,Food
# Create your views here.

# def category_list(request):
#     return HttpResponse("hello world")

def category_list(request):
    all_category = Category.objects.all()
    return render(request,'foods/category_list.html',{"all_category":all_category})

# def food_details(request):
#     return HttpResponse("hello world")

def food_details(request, pk):
    food = Food.objects.get(id=pk)
    return render(request, "food/food_details.html", {"food": food})