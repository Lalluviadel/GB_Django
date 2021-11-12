import hashlib
import random
import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, ValidationError, UserChangeForm

from users.models import User, UserProfile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл.почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            msg = "Email уже используется"
            self.add_error('email', msg)

        new_cleaned_data = super().clean()
        for field in new_cleaned_data:
            if not field == 'image' and len(new_cleaned_data[field]) < 3:
                raise ValidationError('Слишком короткий логин, имя или фамилия.')
        return new_cleaned_data

    def save(self, commit=True):
        user = super().save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'first_name', 'last_name', 'image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

        """ Временно убрала режим 'только для чтения' для email.
         При регистрации через соцсети email не подтягивается, а полю
         email в нашей модели User не допускается быть пустым. Поэтому сигнал
         при редактировании профиля не будет срабатывать, а профиль сохраняться - 
         у нас стоит условие быть валидными обеим формам (а form не будет валидной
         с пустым email).
         Поэтому, сначала следует заполнить поле email, только потом сигнал будет 
         отрабатываеть."""
        # self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    def clean_image(self):
        data = self.cleaned_data['image']
        if data and data.size > 3145728:
            raise forms.ValidationError('Файл с изображением не должен быть больше 3 MB')
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if re.search(r'\d+', data):
            raise ValidationError('Фамилия не должна включать цифры')
        elif len(data) < 3:
            raise ValidationError('Слишком короткая фамилия')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if re.search(r'\d+', data):
            raise ValidationError('Имя не должно включать цифры')
        elif len(data) < 3:
            raise ValidationError('Слишком короткое имя')
        return data


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tagline', 'about', 'gender', 'language')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'gender':
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'form-control'
