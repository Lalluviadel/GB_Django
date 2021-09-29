from django.db import models

from django.http import request ####

from users.models import User
from products.models import Product

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'


    def sum(self):
        return self.quantity * self.product.price


    def total_quantity(self,cumulative_qua=0):
        basket_query_set = Basket.objects.filter(user=self.user.id)
        for item in basket_query_set:
            print(item.quantity)
            cumulative_qua += item.quantity
        return cumulative_qua


    def total_sum(self,cumulative_sum=0):
        basket_query_set = Basket.objects.filter(user=self.user.id)
        for item in basket_query_set:
            cumulative_sum += item.sum()
        return cumulative_sum
