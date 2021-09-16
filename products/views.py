from django.shortcuts import render

def index(request):
    return render(request, 'products/index.html')

def products(request):
    return render(request, 'products/products.html')

def test(request):
    context = {
        'title':'geekshop',
        'header':'Добро пожаловать на сайт',
        'user':'Чубрик',
        'products':[{'name':'Худи черного цвета с монограммами adidas Originals', 'price':'6 090,00'},
                    {'name': 'Синяя куртка The North Face', 'price': '23 725,00'},
                    {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price': '3 390,00'},
        ],
        'products_promo': [{'name': 'Черный рюкзак Nike Heritage', 'price': '2 340,00'},
                           {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'price': '13 590,00'},]
    }
    return render(request, 'products/test.html', context)
