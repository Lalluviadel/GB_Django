from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from products.models import Product
from baskets.models import Basket


class BasketCreateView(CreateView):
    model = Basket
    template_name = 'products/products.html'
    fields = ['product']
    success_url = reverse_lazy('products:index')
    paginate_by = 3


    def get_queryset(self):
        if self.kwargs.keys():
            return Product.objects.filter(category=self.kwargs['category_id'])
        else:
            return Product.objects.all()


    def post(self, request, *args, **kwargs):
        product = self.get_object(Product.objects.filter())
        baskets = Basket.objects.filter(user=request.user, product=product)
        if not baskets.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()


        context = super().get_context_data(**kwargs)
        context.update({'products': Product.objects.all()})
        result = render_to_string('include/product_items.html', context, request=request)
        return JsonResponse({'result': result})


class BasketDeleteView(DeleteView):
    model = Basket
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')


class BasketUpdateView(UpdateView):
    model = Basket
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        basket_id = kwargs.pop('id', None)
        quantity = kwargs.pop('quantity', None)
        if request.is_ajax():
            basket = Basket.objects.get(id=basket_id)
            if quantity > 0:
                basket.quantity = quantity
                basket.save()
            else:
                basket.delete()

            baskets = Basket.objects.filter(user=request.user)
            context = {
                'baskets': baskets,
            }
            result = render_to_string('baskets/baskets.html', context)
            return JsonResponse({'result': result})
        return redirect(self.success_url)
