from django.urls import path

from baskets.views import basket_add, basket_remove

app_name = 'baskets'
urlpatterns = [

    path('add/<int:product_id>/', basket_add, name='basket'),
    path('remove/<int:product_id>/', basket_remove, name='basket_remove'),
#     path('login/', login, name='login'),
#     path('register/', register, name='register'),
#     path('profile/', profile, name='profile'),
#     path('logout/', logout, name='logout'),
]
