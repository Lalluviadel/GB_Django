from django.urls import path
from baskets.views import BasketCreateView, BasketDeleteView, BasketUpdateView

app_name = 'baskets'
urlpatterns = [
    path('add/<int:pk>/', BasketCreateView.as_view(), name='basket'),
    path('remove/<int:pk>/', BasketDeleteView.as_view(), name='basket_remove'),
    path('edit/<int:id>/<int:quantity>/', BasketUpdateView.as_view(), name='basket_edit'),
]


