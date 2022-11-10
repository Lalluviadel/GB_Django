from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.functional import cached_property

from baskets.models import Basket
from products.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлено в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готовится к выдаче'),
        (CANCEL, 'отмена заказа'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус',
                              max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = self.orderitems.select_related()


    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def get_total_quantity(self):
        return sum(list(map(lambda x: x.quantity, self.items)))
        # return sum(list(map(lambda x: x.quantity, self.orderitems.select_related())))

    def get_total_cost(self):
        return sum(list(map(lambda x: x.get_product_cost(), self.items)))
        # return sum(list(map(lambda x: x.quantity, self.orderitems.select_related())))

    def get_items(self):
        # return self.orderitems.select_related()
        return self.items

    def delete(self, using=None, keep_parents=False):
        # for item in self.orderitems.select_related():
        for item in self.items:
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()

    def get_summary(self):
        items = self.items
        return {
            'get_total_cost': sum(list(map(lambda x: x.get_product_cost(), items))),
            'get_total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


class OrderItem(models.Model):
    order = models.ForeignKey(Order,verbose_name='заказ',related_name='orderitems',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='продукты',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',default=0)

    def get_product_cost(self):
        return  self.product.price * self.quantity
        # return self.prod.price * self.quantity

    @staticmethod
    def get_quantity(pk):
        return OrderItem.objects.get(pk=pk).quantity

@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()

@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - instance.get_quantity(int(instance.pk))
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()
