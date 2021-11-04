from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView
from .models import Product, ProductCategory
from django.conf import settings
from django.core.cache import cache


def index(request):
    context = {
        'title': 'Geekshop',
    }
    return render(request, 'products/index.html', context)


def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()

def get_link_product():
    if settings.LOW_CACHE:
        key = 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.all().select_related()
            cache.set(key, link_product)
        return link_product
    else:
        return Product.objects.all().select_related()

class ProductsView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        return context

    def get_queryset(self):
        if self.kwargs.keys():
            # return Product.objects.filter(category_id=self.kwargs['category_id'])

            # Потом раскомментить эту строку!
            # return Product.objects.filter(category_id=self.kwargs['category_id']).select_related('category')
            products = get_link_product()
            return products
        # return Product.objects.all()
        return Product.objects.all().select_related('category')


class ModalWindow(ListView):
    model = Product
    template_name = 'products/modal.html'

    def get(self, request, *args, **kwargs):
        product_id = kwargs.pop('pk', None)
        context = {}
        if request.is_ajax():
            m_product = Product.objects.get(id=product_id)
            context['m_product'] = m_product
            result = render_to_string('products/modal.html', context, request=request)

            return JsonResponse({'result': result})
        return redirect(self)
