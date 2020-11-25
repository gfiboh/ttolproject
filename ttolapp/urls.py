from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import(
    IndexView, ListTeachView, DetailTeachView, CreateTeachView,
    UserContentsView, DeleteTeachView, UpdateTeachView, signupview,
    Login, UserProfileView, UserChangeView,MyPasswordChangeView, 
    MyPasswordChangeDone, UserDeleteView, FindListView,
    CategoryListView,
                    )


app_name = 'ttolapp'

urlpatterns = [
    path('', IndexView.as_view(), name = 'Index'),
    path('list/', ListTeachView.as_view(), name = 'list'),
    path('category/', CategoryListView.as_view(), name = 'category'),
    path('detail/<int:pk>/', DetailTeachView.as_view(), name = 'detail'),
    path('create/', CreateTeachView.as_view(), name = 'create'),
    path('user_contents/', UserContentsView.as_view(), name = 'user_contents'),
    path('delete/<int:pk>/', DeleteTeachView.as_view(), name = 'delete'),
    path('update/<int:pk>/', UpdateTeachView.as_view(), name = 'update'),
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