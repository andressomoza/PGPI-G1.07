from django.shortcuts import render, redirect ,get_object_or_404

from pedidos.models import Pedido
from .forms import IncidenciaForm, IncidenciaEditForm
from .models import Incidencia
from django.contrib.auth.decorators import user_passes_test
from cartech_web.views import is_admin
from django.http import HttpResponseRedirect
from shop.models import Eleccion

def pagina_base(request):
    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)
    return render(request, 'base.html', {'elecciones': elecciones})

def crear_incidencia(request):
    if request.method == 'POST':
        form = IncidenciaForm(request.POST)
        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.estado = 'sin_revisar'
            incidencia.usuario = request.user 
            incidencia.save()
            return HttpResponseRedirect('/incidencias/me')
    else:
        form = IncidenciaForm()

    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)

    return render(request, 'crear_incidencia.html', {'form': form, 'elecciones': elecciones})

def crear_incidencia_pedido(request, id_pedido):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=id_pedido)
        form = IncidenciaForm(request.POST)
        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.usuario = request.user 
            incidencia.pedido = pedido
            incidencia.save()
            return HttpResponseRedirect('/incidencias/me')
    else:
        form = IncidenciaForm()

    return render(request, 'crear_incidencia.html', {'form': form})

@user_passes_test(is_admin)
def listar_incidencias(request):
    urgencia = request.GET.get('urgencia', '')
    
    incidencias = Incidencia.objects.all()
    if urgencia:
        incidencias = incidencias.filter(urgencia=urgencia)

    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)

    context = {
        'incidencias': incidencias,
        'urgencia': urgencia,
        'elecciones': elecciones
    }
    

    return render(request, 'listar_incidencias.html', context)

@user_passes_test(is_admin)
def editar_incidencia(request, id):
    incidencia = get_object_or_404(Incidencia, id=id)

    if request.method == 'POST':
        form = IncidenciaEditForm(request.POST, instance=incidencia)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/incidencias/list')  
    else:
        form = IncidenciaEditForm(instance=incidencia)

    return render(request, 'editar_incidencia.html', {'form': form, 'incidencia': incidencia})

def mis_incidencias(request):
    
    incidencias = Incidencia.objects.filter(usuario = request.user)
    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)

    context = {
        'incidencias': incidencias,
        'elecciones': elecciones

    }

    return render(request, 'mis_incidencias.html', context)