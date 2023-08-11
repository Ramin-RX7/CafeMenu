from django.shortcuts import render
from django.db.models import Count
from django.views import View


from .models import Category,Food



def category_list(request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request,'foods/category_list.html',context)


def category_details(request,id):
    category = Category.objects.get(id=id)
    context = {"category":category, "foods":category.food_set.all()}
    return render(request,'foods/category_details.html',context)


def food_details(request, id):
    food = Food.objects.get(id=id)
    context = {"food": food}
    return render(request, "foods/food_details.html",context)


class SearchView(View):
    def get(self, request):
        searched = request.GET.get('searched')
        FOODS_QUERYSET = Food.objects.filter(title__contains=searched).distinct()
        return render(request, 'foods/search.html', {'searched':searched, "foods":FOODS_QUERYSET})



def menu(request):
    categories = Category.objects.annotate(
            num_foods=Count('food')
        ).filter(num_foods__gt=0).prefetch_related('food_set')
    context = {"categories":categories}
    return render(request, "foods/menu.html", context)
