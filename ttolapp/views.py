from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, \
                                    CreateView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from .models import CustomUser, TeachModel
from .forms import SignupForm, LoginForm, UserChangeForm, CreateTeachForm, FindForm
#クラス汎用ビューのメソッド一覧
#https://selfs-ryo.com/detail/django_class-based-view_methods 参考ページ　

#クラス汎用ビューの属性（変数）一覧

#https://selfs-ryo.com/detail/django_class-based-view_attributes 参考ページ

#ビュークラスの一覧ページ　属性、メソッド、親クラスの一覧があるので便利1
#http://ccbv.co.uk/ 参考ページ


# Create your views here.


class IndexView(TemplateView):
    template_name = 'Index.html'


#ページネーションの参考ページ
#https://djangobrothers.com/blogs/django_pagination/
#https://codor.co.jp/django/how-to-make-pagenation
#request.GETのわかりやすい説明　https://codor.co.jp/django/difference-request-get
class ListTeachView(ListView):
    template_name = 'list.html'
    model = TeachModel
    paginate_by = 6


class DetailTeachView(DetailView):
    template_name = 'detail.html'
    model = TeachModel

#フォームを自作してテンプレートに作成者を入力させるようにする 下に参考ページ
#https://intellectual-curiosity.tokyo/2019/03/19/django%e3%81%aemodelchoicefield%e3%81%ae%e5%88%9d%e6%9c%9f%e5%80%a4%e3%82%92%e8%a8%ad%e5%ae%9a%e3%81%99%e3%82%8b%e6%96%b9%e6%b3%95/
#https://code.i-harness.com/ja-jp/q/47469 ForeignKeyの選択肢はクエリセットで取得される
#https://sleepless-se.net/2019/07/07/django-generic-listview-pagination/　
class CreateTeachView(LoginRequiredMixin, CreateView):
    template_name = 'create.html' 
    form_class = CreateTeachForm
    success_url = reverse_lazy('ttolapp:user_contents')

    #フォームのkwargsには辞書型でフォームの初期値initialが入っている
    #initial内は{'フィールド名':初期値}で値が格納されている
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #CreateTeachFormのteacherフィールドの初期値へアクセス
        kwargs['initial'] = {'teacher': self.request.user}

        return kwargs

#ユーザーが作成したコンテンツを一覧で表示する　この画面から更新・削除するページへ行く
#http://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/
class UserContentsView(ListView):
    template_name = 'user_contents.html'
    model = TeachModel
    paginate_by = 6

    #ページネーション用にクエリセットをユーザーidでフィルターにかけて渡す
    def get_queryset(self):
        teacher_id = self.request.user.id
        queryset = TeachModel.objects.filter(teacher=teacher_id)

        return queryset

    #contextにユーザーのコンテンツ数を渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['contents_count'] = self.get_queryset().count()

        return context



class UpdateTeachView(UpdateView):
    template_name = 'update.html'
    model = TeachModel
    fields = (
        'title', 'category', 'searchword', 'teacher', 'content'
        )
    success_url = reverse_lazy('ttolapp:user_contents')



class DeleteTeachView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = TeachModel
    success_url = reverse_lazy('ttolapp:user_contents')


def signupview(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('ttolapp:login')

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
        #このkwargs.update()はpythonのupdate()関数で、辞書型のkwargsに追加または更新をしている
        kwargs.update(
            {#self.request.userでログイン中のユーザー情報を取得
                'username': self.request.user.username,
                'email': self.request.user.email
            }
        )

        return kwargs


#https://qiita.com/t-iguchi/items/67430e164de0e6701dc8 参考ページ　パスワード変更
#パスワード変更画面
class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    #テンプレートはtemplatesフォルダ内にregistrationフォルダを作成し、
    # その中にpassword_change_form.html,password_change_done.htmlを作った

    template_name = 'registration/password_change_form.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('ttolapp:password_change_done')

    #テンプレートに各パスワードのラベルとして使うための文字をビューに持たせる
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['old_pass'] = '現在のパスワード'
        context['new_pass1'] = '新しいパスワード'
        context['new_pass2'] = '新しいパスワードの再確認'

        return context


#パスワード変更完了画面
class MyPasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'


#ユーザー削除（退会）画面
#https://teratail.com/questions/208698 参考ページ
#https://jyouj.hatenablog.com/entry/2018/11/24/172910 参考ページ　
#※ただし、カスタムユーザーモデルではUserPassesTestMixinはpkかslugを定義しないとうまくいかない
class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'userdelete.html'
    model = CustomUser
    success_url = reverse_lazy('ttolapp:Index')


#検索ページ リスト表示とフォームを利用する
class FindListView(ListView):
    template_name = 'find.html'
    model = TeachModel
    paginate_by = 6

    #フォームの入力値をバリデーションチェックしてからmodel内を検索
    #クエリセットに検索結果を入れる
    def get_queryset(self):
        form = FindForm(self.request.GET)
        form.is_valid()
        search_word = form.cleaned_data['find']
        queryset = TeachModel.objects.filter(
                Q(title__icontains=search_word) | Q(searchword__icontains=search_word)
                )
        return queryset

    #検索結果によってヒットした件数か見つからなかったことを表示するcontextを渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['find_count'] = self.get_queryset().count()

        if context['find_count'] == 0:
            context['msg'] = '見つかりませんでした'

        return context