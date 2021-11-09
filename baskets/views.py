from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from geekshop.mixin import UserDispatchMixin
from products.models import Product
from baskets.models import Basket


class BasketCreateView(CreateView, UserDispatchMixin):
    model = Basket
    template_name = 'products/products.html'
    fields = ['product']
    success_url = reverse_lazy('products:index')

    def post(self, request, *args, **kwargs):
        product = self.get_object(Product.objects.filter())
        baskets = Basket.objects.filter(user=request.user, product=product)
        if not baskets.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()

        request.GET = request.GET.copy()

        source_page = request.POST['current_page']
        _cat = source_page.split('category')
        _page = source_page.split('page=')
        if len(_cat) > 1:
            request.GET['category_id'] = _cat[1].split('/')[1]
        if len(_page) > 1:
            request.GET['page'] = int(_page[1])

        result = render_to_string('include/product_items.html', request=request)
        return JsonResponse({'result': result})


class BasketDeleteView(DeleteView):
    model = Basket
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')


class BasketUpdateView(UpdateView, UserDispatchMixin):
    model = Basket
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'
    fields = ['product']

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

            result = render_to_string('baskets/baskets.html', request=request)

            return JsonResponse({'result': result})
        return redirect(self)
