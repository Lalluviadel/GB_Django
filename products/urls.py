from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ProductsView, ModalWindow, ProductDetail

app_name = 'products'
urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsView.as_view(), name='category'),
    path('page/<int:page_id>/', ProductsView.as_view(), name='page'),

    # path('modal/<int:product_id>/', modal_window, name='modal'),
    path('modal/<int:pk>/', ModalWindow.as_view(), name='modal'),
    path('detail/<int:pk>/', cache_page(3600)(ProductDetail.as_view()), name='detail'),
]
