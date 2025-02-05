from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth.models import User


class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Оставьте ваш отзыв'
    }))

    class Meta:
        model = Reviews
        fields = ('text',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Логин'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Юзернейм'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Фамилия'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Почта'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EditAccountForm(UserChangeForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'class': 'contact__section-input'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    street = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    home = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    flat = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    class Meta:
        model = Profile
        fields = ('phone', 'city', 'street', 'home', 'flat')


class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',

        'placeholder': 'Имя получателя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',

        'placeholder': 'Фамилия получателя'
    }))

    telegram = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',

        'placeholder': 'Телеграм получателя'
    }))

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'last_name')


class ShippingForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',

        'placeholder': 'Адрес '
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Номер телефона'
    }))

    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-input',
        'placeholder': 'Комментарий к заказу (необязательно)',
        'rows': 5,
        'cols': 40
    }))

    region = forms.ModelChoiceField(queryset=Region.objects.all(), widget=forms.Select(attrs={
        'class': 'form-input',
        'placeholder': 'Выберите регион'

    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Город'
    }))

    class Meta:
        model = ShippingAddress
        fields = ('region', 'city', 'address', 'phone', 'comment')

