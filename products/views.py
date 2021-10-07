from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product,ProductCategory


def index(request):
    context = {
        'title': 'geekshop',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_id=1):
    products = Product.objects.filter(category_id=category_id) \
        if category_id is not None else Product.objects.all()
    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {
        'title': 'Каталог',
        'categorys': ProductCategory.objects.all(),
        'products': products_paginator,
        }
    # Lesson 8: дополнить/изменить значение по ключу в словаре context можно и так:
    # context.update({'products': products_paginator})
    return render(request, 'products/products.html', context)
