from django.shortcuts import render
from django.views.generic import TemplateView



class IndexTemplateView(TemplateView):
    template_name = "index.html"


class AboutUsTemplateView(TemplateView):
    template_name = "core/about_us.html"
