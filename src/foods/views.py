from django.shortcuts import render
from django.http import Http404
from django.db.models import Q
from .models import Category,Food


def category_list(request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request,'foods/category_list.html',context)


def category_details(request,id):
    category = Category.objects.get(id=id)
    context = {"category":category}
    return render(request,'foods/category_details.html',context)


def food_details(request, id):
    food = Food.objects.get(id=id)
    context = {"food": food}
    return render(request, "foods/food_details.html",context)


def search(request):
    if request.method == "GET":
        searched = request.GET.get('searched')
        FOODS_QUERYSET = Food.objects.filter(
        Q(title__contains=searched).distinct())
        return render(request, 'foods/search.html', {'searched':searched, "foods":FOODS_QUERYSET})
    else:
        raise Http404


def menu(request):
    return render(request, "foods/menu.html")

