from django.urls import path
from .views import ProductsView, ModalWindow, ProductDetail

app_name = 'products'
urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsView.as_view(), name='category'),
    path('page/<int:page_id>/', ProductsView.as_view(), name='page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
    path('modal/<int:pk>/', ModalWindow.as_view(), name='modal'),

]
