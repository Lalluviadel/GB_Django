from .views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView
from django.urls import path

app_name = 'admins'
urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins_user'),
    path('users-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
]
