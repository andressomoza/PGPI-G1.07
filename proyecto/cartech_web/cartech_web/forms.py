from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    direccion = forms.CharField(max_length=255)
    ciudad = forms.CharField(max_length=100)
    codigo_postal = forms.CharField(max_length=10)
    


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'direccion', 'ciudad', 'codigo_postal')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.direccion = self.cleaned_data['direccion']
        user.direccion = self.cleaned_data['ciudad']
        user.direccion = self.cleaned_data['codigo_postal']
        
        if commit:
            user.save()
        return user
