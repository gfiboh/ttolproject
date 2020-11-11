from django import forms
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm
#https://qiita.com/j54854/items/b25a85ddf41b6d8ffab6 参考ページ　ここを見てフォームを作る
#https://hombre-nuevo.com/python/python0038/ 参考ページ　DoesNotExistの例外処理の仕方　
#http://retasu0.com/?p=96 参考ページ　ログイン時の表示ページを変える設定

class SignupForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder':'パスワード'}),
        }

    password2 = forms.CharField(
        label = '確認用パスワード',
        required = True,
        strip = False,
        widget = forms.PasswordInput(attrs={'placeholder':'確認用パスワード'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder':'ユーザー名'}
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 3:
            raise forms.ValidationError(
            '3文字以上で入力してください'
        )

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
            'そのユーザー名は使えません'
        )

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 5:
            raise forms.ValidationError(
            '5文字以上で入力してください'
        )

        return password

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and (password != password2):
            raise forms.ValidationError(
            'パスワードと確認用パスワードが一致していません'
            )


class LoginForm(AuthenticationForm):
#AuthenticationFormクラスのフィールドはusername,password,error_messages 参考ページは下のURL
#https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder':'ユーザー名'}
        self.fields['password'].widget.attrs = {'placeholder':'パスワード'}
#エラーメッセージを日本語にする
        self.error_messages = {
            'invalid_login': "正しいユーザー名とパスワードを入力してください",
            'inactive':"このアカウントは非アクティブです",
        }

#ユーザー情報変更フォーム（パスワードはここでは変更出来ない）
#https://django.kurodigi.com/profile-change/ 参考ページ
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',        
        )
        #usernameのhelp_textに名前の入力に使える文字の説明のテキストを非表示にする
        help_texts = {'username': None}
        

    def __init__(self,username=None, email=None, *args, **kwargs):
        #dict型のkwargs変数にlabel_suffixでラベル名:とされるのをラベル名->とする
        kwargs.setdefault('label_suffix', '->')
        super().__init__(*args, **kwargs)

        #ユーザーの更新前の情報をフォームに入れる
        if username:
            self.fields['username'].widget.attrs['value'] = username
        if email:
            self.fields['email'].widget.attrs['value'] = email

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()
