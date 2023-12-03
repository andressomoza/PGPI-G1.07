from django.shortcuts import render, get_object_or_404
from shop.models import Eleccion, Coche, Accesorio
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'shop/home.html')

#@login_required
def listar_carrito(request):
    usuario = request.user.id
    elecciones = Eleccion.objects.all()
    elecciones = elecciones.filter(usuario_id=usuario).values()

    return render(request, 'listar_carrito.html', {'elecciones': list(elecciones)})
