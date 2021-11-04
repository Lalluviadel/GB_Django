from django.db import models
from django.utils.functional import cached_property

from users.models import User
from products.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super(BasketQuerySet, self).delete()



class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        # self.product.queryset = Product.objects.all().select_related('price')
        return self.quantity * self.product.price

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @staticmethod
    def total_quantity(user):
        baskets = Basket.objects.filter(user=user)
        # baskets = self.get_items_cached
        return sum(basket.quantity for basket in baskets)

    @staticmethod
    def total_sum(user):
        basket_query_set = Basket.objects.filter(user=user).select_related()
        # basket_query_set = self.get_items_cached
        return sum(basket.sum() for basket in basket_query_set)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity


