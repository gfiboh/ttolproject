from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import IndexView, ListTeach, DetailTeach, \
                    CreateTeach, DeleteTeach, signupview, \
                    Login, UserProfileView, UserChangeView, \
                    MyPasswordChangeView, MyPasswordChangeDone, \
                    UserDeleteView, FindListView


app_name = 'ttolapp'

urlpatterns = [
    path('', IndexView.as_view(), name = 'Index'),
    path('list/', ListTeach.as_view(), name = 'list'),
    path('detail/<int:pk>/', DetailTeach.as_view(), name = 'detail'),
    path('create/', CreateTeach.as_view(), name = 'create'),
    path('delete/<int:pk>/', DeleteTeach.as_view(), name = 'delete'),
    path('signup/', signupview, name = 'signup'),
    path('login/', Login.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('change/', UserChangeView.as_view(), name = 'change'),
    #パスワード変更用にdjango.contrib.auth.urlsのPasswordChangeView,PasswordChangeDoneViewを使う
    #urlは 'accounts/password_change' で表示される
    #https://django.kurodigi.com/password-change/ 参考ページ　パスワード変更画面
    path('password_change/', MyPasswordChangeView.as_view(), name = 'password_change'),
    path('password_change/done/', MyPasswordChangeDone.as_view(), name = 'password_change_done'),
    path('userdelete/<int:pk>/', UserDeleteView.as_view(), name = 'userdelete'),
    path('find/', FindListView.as_view(), name = 'find'),
]