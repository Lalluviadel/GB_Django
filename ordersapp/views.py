from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem
from products.models import Product


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop | Создать заказ'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm,
                                                     extra=basket_items.count())
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price * basket_items[num].quantity

            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop | Обновить заказ'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            # Проверить потом, вот это улучшает или нет (или оно в методичке было)
            # queryset = self.object.orderitems.select_related()
            # formset = OrderFormSet(instance=self.object, queryset=queryset)
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price * form.initial['quantity']

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


class OrderDetail(DetailView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop | Просмотр заказа'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headings'] = ['', 'Категория', 'Товар', 'Цена, руб/шт',
                               'Кол-во, шт', 'Общая сумма, руб', ]
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    if request.is_ajax():
        result = render_to_string('ordersapp/includes/inc_orders_table.html', request=request)
        return JsonResponse({'result': result})

    return HttpResponseRedirect(reverse('orders:list'))


def basket_clear(request):
    basket_items = Basket.objects.filter(user=request.user)
    basket_items.delete()

    if request.is_ajax():
        result = render_to_string('baskets/baskets.html')
        return JsonResponse({'result': result})
    return HttpResponseRedirect(reverse('users:profile'))


# Для приделывания робокассы:
# def payment_result(request):
#     status = request.GET.get('ik_inv_st')
#     if status == 'success':
#         order_pk = request.GET.get('ik_pm_no')
#         order_item = Order.objects.get(pk=order_pk)
#         order_item.status = Order.PAID
#         order_item.save()
#     return HttpResponseRedirect(reverse('orders:list'))

def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.get(pk=pk)
        if product:
            return JsonResponse({'price': product.price})

    return JsonResponse({'price': 0})
