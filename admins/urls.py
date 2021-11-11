from django.urls import path

from .views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView, \
    CategoriesListView, CategoriesUpdateView, CategoriesCreateView, CategoriesDeleteView, \
    ProductsListView, ProductsUpdateView, ProductsCreateView, ProductsDeleteView, user_is_staff

app_name = 'admins'
urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins_user'),
    path('users-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),

    path('users-is-staff/<int:pk>/', user_is_staff, name='admins_user_is_staff'),

    path('categories/', CategoriesListView.as_view(), name='admins_categories'),
    path('categories/create/', CategoriesCreateView.as_view(), name='admins_category_create'),
    path('categories/update/<int:pk>/', CategoriesUpdateView.as_view(), name='admins_category_update'),
    path('categories/delete/<int:pk>/', CategoriesDeleteView.as_view(), name='admins_category_delete'),

    path('products/', ProductsListView.as_view(), name='admins_products'),
    path('products/update/<int:pk>/', ProductsUpdateView.as_view(), name='admins_product_update'),
    path('products/create/', ProductsCreateView.as_view(), name='admins_product_create'),
    path('products/delete/<int:pk>/', ProductsDeleteView.as_view(), name='admins_product_delete'),
]
