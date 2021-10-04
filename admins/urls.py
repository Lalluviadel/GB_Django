import admins.views as admins
from .views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView, \
    CategoriesListView, CategoriesUpdateView, CategoriesCreateView, CategoriesDeleteView
from django.urls import path

app_name = 'admins'
urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins_user'),
    path('users-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),

    path('categories/', CategoriesListView.as_view(), name='admins_categories'),
    path('categories/create/', CategoriesCreateView.as_view(), name='admins_category_create'),
    path('categories/update/<int:pk>/', CategoriesUpdateView.as_view(), name='admins_category_update'),
    path('categories/delete/<int:pk>/', CategoriesDeleteView.as_view(), name='admins_category_delete'),

]
