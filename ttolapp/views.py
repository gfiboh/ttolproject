from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, \
                                    CreateView, DeleteView
from .models import CustomUser, TeachModel
from django.urls import reverse_lazy
from .forms import SignupForm

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

def signupview(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ttolapp:Index')

    else:
        form = SignupForm()

    context = {'form':form}
    return render(request, 'signup.html', context)