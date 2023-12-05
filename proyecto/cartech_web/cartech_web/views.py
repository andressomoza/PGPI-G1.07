from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login
from .forms import CustomUserCreationForm


def is_admin(user):
    return user.is_authenticated and user.is_staff
# Create your views here.
@login_required
def index(request):
    return render(request, 'plantilla/base.html')

def salir(request):
    logout(request)
    return redirect('/')

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

def bad_request(request, exception):
    return render(request, 'errors/400_bad_request.html', status=400)

def forbidden(request, exception):
    return render(request, 'errors/403_forbidden.html', status=403)

def not_found(request, exception):
    return render(request, 'errors/404_not_found.html', status=404)

def internal_server_error(request):
    return render(request, 'errors/500_internal_server_error.html', status=500)