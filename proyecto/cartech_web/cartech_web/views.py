from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login



# Create your views here.
@login_required
def index(request):
    return render(request, 'plantilla/base.html')

def salir(request):
    logout(request)
    return redirect('/')

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Resto del código para el registro exitoso
            return redirect('/')  # Cambia 'index' a la URL a la que quieras redirigir
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
