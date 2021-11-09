from baskets.models import Basket
from products.models import ProductCategory, Product
from ordersapp.models import Order
import products.views


def basket(request):
    baskets_list = []
    if request.user.is_authenticated:
        baskets_list = Basket.objects.filter(user=request.user)
    return {
        'baskets': baskets_list,
    }


def categories(request):
    return {
        'categories': ProductCategory.objects.all(),
    }


def orders(request):
    if request.user.is_authenticated:
        return {
            'orders': Order.objects.filter(user=request.user)
        }
    else:
        return {
            'orders': ''
        }


def product_set(request, current_category=None):
    page = request.GET.get('page')
    if 'category_id' in request.resolver_match.kwargs:
        current_category = request.resolver_match.kwargs['category_id']
    elif 'category_id' in request.GET:
        current_category = request.GET.get('category_id')

    if current_category:
        queryset = Product.objects.filter(category_id=current_category)
        product_set = products.views.paginate_me(queryset, page)
        return {
            'product_set': product_set
        }
    else:
        queryset = Product.objects.all()
        product_set = products.views.paginate_me(queryset, page)
        return {
            'product_set': product_set
        }
