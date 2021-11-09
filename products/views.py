from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from .models import Product, ProductCategory


def index(request):
    context = {
        'title': 'Geekshop',
    }
    return render(request, 'products/index.html', context)


def get_product(pk):
    # if settings.LOW_CACHE:
    #     key = f'product{pk}'
    #     product = cache.get(key)
    #     if product is None:
    #         product = get_object_or_404(Product,pk=pk)
    #         cache.set(key, product)
    #     return product
    # else:
    #     return get_object_or_404(Product,pk=pk)
    return get_object_or_404(Product, pk=pk)


class ProductsView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        return context

    # def get_queryset(self):
    #     if self.kwargs.keys():
    #         return Product.objects.filter(category_id=self.kwargs['category_id'])
    #     return Product.objects.all()


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


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()
        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = ProductCategory.objects.all()
        return context


def paginate_me(queryset, num):
    paginator = Paginator(queryset, per_page=3)
    try:
        products_paginator = paginator.page(num)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    return products_paginator
