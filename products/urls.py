from django.urls import path
from .views import ProductsView, modal_window

app_name = 'products'
urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsView.as_view(), name='category'),
    path('page/<int:page_id>/', ProductsView.as_view(), name='page'),

    path('modal/<int:product_id>/', modal_window, name='modal'),
]
