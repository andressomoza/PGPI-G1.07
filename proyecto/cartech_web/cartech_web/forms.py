from django import forms

from user.models import User
from .choices import MetodoPago
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    direccion = forms.CharField(max_length=255, required=False)
    ciudad = forms.CharField(max_length=100, required=False)
    codigo_postal = forms.CharField(max_length=10, required=False)
    metodo_pago = forms.ChoiceField(choices=MetodoPago.choices_with_empty_option, required=False)
    


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'direccion', 'ciudad', 'codigo_postal', 'metodo_pago')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.direccion = self.cleaned_data['direccion']
        user.ciudad = self.cleaned_data['ciudad']
        user.codigo_postal = self.cleaned_data['codigo_postal']
        user.metodo_pago = self.cleaned_data['metodo_pago']
        
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'direccion', 'ciudad', 'codigo_postal', 'metodo_pago')