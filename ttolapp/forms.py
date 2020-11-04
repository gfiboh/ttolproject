from django import forms
from .models import CustomUser

#https://qiita.com/j54854/items/b25a85ddf41b6d8ffab6 参考ページURL　ここを見てフォームを作る
#http://retasu0.com/?p=96 参考ページURL　ログイン時の表示ページを変える設定

class SignupForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

    password2 = forms.CharField(
        label = '確認用パスワード',
        required = True,
        strip = False,
        widget = forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
            'このユーザー名はすでに存在します'
        )

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            raise forms.ValidationError(
            '5文字以上で入力してください'
        )

        return password

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError(
            'パスワードと確認用パスワードが一致していません'
        )

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        new_user = CustomUser.objects.create_user(username = username)
        new_user.set_password(password)
        new_user.save()
