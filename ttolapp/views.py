from django.shortcuts import render
from django.views.generic import TemplateView
from .models import CustomUser, TeachModel
from django.urls import reverse_lazy

# Create your views here.

class IndexView(TemplateView):
    template_name = 'Index.html'