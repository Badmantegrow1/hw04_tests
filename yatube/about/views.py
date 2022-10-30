from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='about/author.html')


class AboutTechView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='about/tech.html')
