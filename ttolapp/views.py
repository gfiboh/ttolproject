from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, \
                                    CreateView, DeleteView
from django.urls import reverse_lazy
from .models import CustomUser, TeachModel
from .forms import SignupForm, LoginForm


# Create your views here.

class IndexView(TemplateView):
    template_name = 'Index.html'

class ListTeach(ListView):
    template_name = 'list.html'
    model = TeachModel

class DetailTeach(DetailView):
    template_name = 'detail.html'
    model = TeachModel


class CreateTeach(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    model = TeachModel
    fields = (
        'title',
        'category',
        'serchword',
        'content'
    )

    success_url = reverse_lazy('list')


class DeleteTeach(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = TeachModel

    success_url = reverse_lazy('list')

def signupview(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('ttolapp:Index')

    else:
        form = SignupForm()

    context = {'form':form}
    return render(request, 'signup.html', context)

#https://blog.narito.ninja/detail/40 参考ページ　ログイン、ログアウトについて
#LoginViewクラスはAuthenticationFormクラスを使っている
class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
