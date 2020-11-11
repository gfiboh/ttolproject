from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, \
                                    CreateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import CustomUser, TeachModel
from .forms import SignupForm, LoginForm, UserChangeForm
#クラス汎用ビューのメソッド一覧
#https://selfs-ryo.com/detail/django_class-based-view_methods 参考ページ　
#クラス汎用ビューの属性（変数）一覧
#https://selfs-ryo.com/detail/django_class-based-view_attributes 参考ページ


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


#https://django.kurodigi.com/custamize-user/　参考ページ　カスタムユーザープロフィール表示
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    #このメソッドでユーザーidを取得
    def get_queryset(self):
        return CustomUser.objects.get(id = self.request.user.id)


class UserChangeView(LoginRequiredMixin, FormView):
    template_name = 'change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('ttolapp:profile')

    #バリデーションOKのときの処理
    def form_valid(self, form):
        #フォームの自作updateメソッドにログインユーザー情報を渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #更新前のユーザー情報をkwargsとして渡す
        kwargs.update(
            {#self.request.userでログイン中のユーザー情報を取得
                'username': self.request.user.username,
                'email': self.request.user.email
            }
        )

        return kwargs
    
#https://qiita.com/t-iguchi/items/67430e164de0e6701dc8 参考ページ　パスワード変更
#パスワード変更画面
"""
class PsswordChange(LoginRequiredMixin, PasswordChangeView):
    #テンプレートはtemplatesフォルダ内にregistrationフォルダを作成し、
    # その中にpassword_change_form.html,password_change_done.htmlを作った
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

#パスワード変更完了画面
class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'
"""