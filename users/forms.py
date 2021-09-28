from django.contrib.auth.forms import AuthenticationForm, \
     UserCreationForm, ValidationError, UserChangeForm
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self,*args,**kwargs):
        super(UserLoginForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

    def __init__(self,*args,**kwargs):
        super(UserRegisterForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл.почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean(self):
        '''Checks name fields length'''
        new_cleaned_data = super(UserRegisterForm, self).clean()
        u_name = self.cleaned_data['username']
        f_name = self.cleaned_data['first_name']
        l_name = self.cleaned_data['last_name']
        if len(u_name) < 3 or len(f_name) < 3 or len(l_name) < 3 :
            raise ValidationError('Слишком короткий логин, имя или фамилия!')
        return new_cleaned_data


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(),required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image',)

    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    def clean_image(self):
        data = self.cleaned_data['image']
        if data:
        # без этого условия при попытке сохранить изменения профиля на сайте
        # без загрузки картинки пользователь получит ошибку
            if data.size > 1000000:
                raise forms.ValidationError('Файл слишком большой')
        return data
