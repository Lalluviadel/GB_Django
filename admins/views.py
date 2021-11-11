from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.dispatch import receiver
from django.db.models.signals import pre_save


from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryProductsForm, ProductsForm \
    # CategoryUpdateFormAdmin
from geekshop.mixin import CustomDispatchMixin
from products.models import ProductCategory, Product
from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Регистрация'
        return context


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-read.html'
    success_url = reverse_lazy('admins:admins_user')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.id != kwargs['pk']:
            self.object.is_active = False if self.object.is_active == True else True
        # self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        objects = User.objects.all()
        context = {'users': objects}
        self.delete(request, *args, **kwargs)
        result = render_to_string('included/table-users.html', context, request=request)
        return JsonResponse({'result': result})


class CategoriesListView(ListView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Категории'
        context['objects']: ProductCategory.objects.all().select_related()
        return context


class CategoriesUpdateView(UpdateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    # !!!!!!
    # form_class = CategoryUpdateFormAdmin
    # !!!!!!
    form_class = CategoryProductsForm
    success_url = reverse_lazy('admins:admins_categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление категории'
        return context

    # !!!!!!
    # def form_valid(self, form):
    #     if 'discount' in form.cleaned_data:
    #         discount = form.cleaned_data['discount']
    #         if discount:
    #             print(f'применяется скидка {discount} %  к товарам категории {self.object.name}')
    #             self.object.product_set.update(price=F('price')*(1-discount/100))
    #             db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
    #         return HttpResponseRedirect(self.get_success_url())
    # !!!!!!


class CategoriesCreateView(CreateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-create.html'
    form_class = CategoryProductsForm
    success_url = reverse_lazy('admins:admins_categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Создание категории'
        return context


class CategoriesDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    success_url = reverse_lazy('admins:admins_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.product_set.update(available = False)
        self.object.available = False if self.object.available == True else True
        # self.object.available = False
        self.object.save()

    def post(self, request, *args, **kwargs):
        category = ProductCategory.objects.all()
        context = {'object_list': category}
        self.delete(request, *args, **kwargs)
        result = render_to_string('included/table-categories.html', context, request=request)
        return JsonResponse({'result':result})

class ProductsListView(ListView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Продукты'
        context['objects'] = Product.objects.all().select_related('category')
        return context


class ProductsUpdateView(UpdateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-update-delete.html'
    form_class = ProductsForm
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление продукта'
        return context


class ProductsCreateView(CreateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-create.html'
    form_class = ProductsForm
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка | Создание продукта'
        return context


class ProductsDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    success_url = reverse_lazy('admins:admins_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.available = False if self.object.available == True else True
        # self.object.available = False
        self.object.save()

    def post(self, request, *args, **kwargs):
        objects = Product.objects.all()
        context = {'objects': objects}
        self.delete(request, *args, **kwargs)
        result = render_to_string('included/table-products.html', context, request=request)
        return JsonResponse({'result': result})
        # return HttpResponseRedirect(self.get_success_url())

# !!!!!!!!
def db_profile_by_type(prefix, type, queries):
   update_queries = list(filter(lambda x: type in x['sql'], queries))
   print(f'db_profile {type} for {prefix}:')
   [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
   if instance.pk:
       if instance.available:
           instance.product_set.update(available=True)
       else:
           instance.product_set.update(available=False)

       db_profile_by_type(sender, 'UPDATE', connection.queries)
# !!!!!!!!


def user_is_staff(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_staff = False if user.is_staff == True else True
    user.save()
    if request.is_ajax():
        objects = User.objects.all()
        context = {'users': objects}
        result = render_to_string('included/table-users.html', context, request=request)
        return JsonResponse({'result': result})
    return HttpResponseRedirect(reverse('admins:admins_user'))