from django import forms
from django.forms import ModelForm

from products.models import ProductCategory, Product
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password1', 'password2', 'image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class UserAdminProfileForm(UserProfileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class CategoryProductsForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'discount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

# # !!!!!!!!!!
# class CategoryUpdateFormAdmin(forms.ModelForm):
#     discount = forms.IntegerField(widget=forms.NumberInput(), label='скидка', required=False, min_value=0, max_value=90,
#                                   initial=0)
#
#     class Meta:
#         model = ProductCategory
#         fields = ('name', 'description', 'discount')
#
#     def __init__(self,*args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control py-4'
# !!!!!!!!!!

class ProductsForm(ModelForm):
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all().select_related(),
                                      empty_label=None)
    image = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image' or field_name == 'category':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'
