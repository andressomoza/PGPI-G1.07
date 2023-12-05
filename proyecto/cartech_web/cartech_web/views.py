from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from .forms import CustomUserCreationForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from user.models import User
from .forms import CustomUserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
import random
import string




class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password.html'
    success_url = reverse_lazy('shop:home')


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

def create_default_user(request):

    base_username = 'default_user'
    base_email = 'default_user@example.com'
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    default_user_data = {
        'username': f'{base_username}_{suffix}',
        'password': 'password123',  
        'email': f'{base_email}_{suffix}',
    }
    user_exists = User.objects.filter(username=default_user_data['username']).exists()

    if not user_exists:
        user = User.objects.create_user(**default_user_data)

        
        user = authenticate(request, username=user.email, password=default_user_data['password'])
        login(request, user)
    
    return redirect('/')  

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('shop:home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Puedes realizar acciones adicionales aquí si lo necesitas
        return super().form_valid(form)

def bad_request(request, exception):
    return render(request, 'errors/400_bad_request.html', status=400)

def forbidden(request, exception):
    return render(request, 'errors/403_forbidden.html', status=403)

def not_found(request, exception):
    return render(request, 'errors/404_not_found.html', status=404)

def internal_server_error(request):
    return render(request, 'errors/500_internal_server_error.html', status=500)


    