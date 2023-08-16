from typing import Any, Dict
from django.shortcuts import render
from django.db.models import Count
from django.views import View
from django.views.generic import ListView,DetailView


from .models import Category,Food


class CategoryListView(ListView):
    model = Category
    template_name = 'foods/category_list.html'
    context_object_name = "categories"



class CategoryDetailView(DetailView):
    model = Category
    template_name = 'foods/category_details.html'
    context_object_name = 'category'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['foods'] = category.food_set.all()
        return context


class FoodDetailView(DetailView):
    model=Food
    template_name="foods/food_details.html"
    pk_url_kwarg='id'
    context_object_name='food'


class SearchView(View):
    def get(self, request):
        searched = request.GET.get('searched')
        FOODS_QUERYSET = Food.objects.filter(title__contains=searched).distinct()
        return render(request, 'foods/search.html', {'searched':searched, "foods":FOODS_QUERYSET})



class MenuListView(ListView):
    model = Category
    template_name = 'foods/menu.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            num_foods=Count('food')
        ).filter(num_foods__gt=0).prefetch_related('food_set')
        return queryset

