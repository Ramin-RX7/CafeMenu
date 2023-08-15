from django.shortcuts import render
from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class AboutUsTemplateView(TemplateView):
    template_name = "main/about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

