from django.contrib.auth import views as auth_views
from django.urls import path
from .views import IndexView, ListTeach, DetailTeach, \
                    CreateTeach, DeleteTeach, signupview, \
                    Login


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
]