from django.shortcuts import render

from .models import Product,ProductCategory

def index(request):
    context = {
        'title': 'geekshop',
    }
    return render(request, 'products/index.html', context)


def products(request):
    title = 'geekshop'
    categories = ProductCategory.objects.all()
    product = Product.objects.all()
    content = {'title': title, 'products': product, 'category': categories}
    return render(request, 'products/products.html', content)
