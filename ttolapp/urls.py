from django.urls import path
from .views import IndexView, ListTeach, DetailTeach, \
                    CreateTeach, DeleteTeach


app_name = 'ttolapp'

urlpatterns = [
    path('', IndexView.as_view(), name = 'Index'),
    path('list/', ListTeach.as_view(), name = 'list'),
    path('detail/<int:pk>/', DetailTeach.as_view(), name = 'detail'),
    path('create/', CreateTeach.as_view(), name = 'create'),
    path('delete/<int:pk>/', DeleteTeach.as_view(), name = 'delete'),
]