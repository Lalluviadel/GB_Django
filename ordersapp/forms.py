from django import forms
from ordersapp.models import Order, OrderItem
from products.models import Product
from users.models import User


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        # self.fields['user'].queryset = User.objects.all().select_related()
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemsForm(forms.ModelForm):

    price = forms.CharField(label='цена',required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):

        # self.fields['order'].queryset = Order.objects.all().select_related()
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all().select_related()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
