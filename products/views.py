from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Product, ProductCategory


def index(request):
    context = {
        'title': 'Geekshop',
    }
    return render(request, 'products/index.html', context)


class ProductsView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context.update({'categorys': ProductCategory.objects.all()})
        return context

    def get_queryset(self):
        if self.kwargs.keys():
            return Product.objects.filter(category_id=self.kwargs['category_id'])
        else:
            return Product.objects.all()
