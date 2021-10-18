from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Product


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
        return context

    def get_queryset(self):
        if self.kwargs.keys():
            return Product.objects.filter(category_id=self.kwargs['category_id'])
        return Product.objects.all()



def modal_window(request, product_id):
    m_product = get_object_or_404(Product, id=product_id)
    context = {}
    context['m_product'] = m_product
    return render(request, 'products/modal.html', context)
