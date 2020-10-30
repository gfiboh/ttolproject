from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, \
                                    CreateView, DeleteView
from .models import CustomUser, TeachModel
from django.urls import reverse_lazy

# Create your views here.

class IndexView(TemplateView):
    template_name = 'Index.html'

class ListTeach(ListView):
    template_name = 'list.html'
    model = TeachModel

class DetailTeach(DetailView):
    template_name = 'detail.html'
    model = TeachModel

class CreateTeach(CreateView):
    template_name = 'create.html'
    model = TeachModel
    fields = (
        'title',
        'category',
        'serchword',
        'content'
    )

    success_url = reverse_lazy('list')

class DeleteTeach(DeleteView):
    template_name = 'delete.html'
    model = TeachModel

    success_url = reverse_lazy('list')