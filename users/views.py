from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import FormView, UpdateView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, CustomDispatchMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Geekshop - Авторизация',
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)
from users.models import User


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Geekshop - Авторизация'


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {
#         'title': 'Geekshop - Регистрация',
#         'form': form,
#     }
#     return render(request, 'users/register.html', context)
class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Geekshop - Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect(self.success_url)
        return redirect(self.success_url)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно внесли изменения')
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             messages.error(request, 'Профиль не сохранен')
#     else:
#         form = UserProfileForm(instance=request.user)
#
#         # Lesson_06 teacher's solution #1
#         # total_sum = 0
#         # total_quantity = 0
#         # baskets = Basket.objects.filter(user=request.user)
#         # for basket in baskets:
#         #     total_quantity += basket.quantity
#         #     total_sum += basket.sum()
#
#
#         # Lesson_06 teacher's solution #2
#         # baskets = Basket.objects.filter(user=request.user)
#         # total_sum = sum(basket.sum() for basket in baskets)
#         # total_quantity = sum(basket.quantity for basket in baskets)
#
#     context = {
#         'title': 'Geekshop - Профайл',
#         # 'form': UserProfileForm(instance=request.user),
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#
#         # Lesson_06 teacher's solution #1, 2
#         # 'total_sum': total_sum,
#         # 'total_quantity': total_quantity,
#
#     }
#     return render(request,'users/profile.html',context)
class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Geekshop - Профиль'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    # @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    # def dispatch(self, request, *args, **kwargs):
    #     return super(ProfileFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST,files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))

class Logout(LogoutView):
    template_name = 'products/index.html'
