from django.shortcuts import render, redirect ,get_object_or_404
from .forms import IncidenciaForm
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
            incidencia.usuario = request.user 
            incidencia.save()
            return HttpResponseRedirect('/incidencias/me')
    else:
        form = IncidenciaForm()

    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)

    return render(request, 'crear_incidencia.html', {'form': form, 'elecciones': elecciones})

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
def borrar_incidencia(request, id):
    incidencia = get_object_or_404(Incidencia, id=id)

    if request.method == 'POST':
        incidencia.delete()
        return HttpResponseRedirect('/incidencias/list')  

    return render(request, 'borrar_incidencia.html', {'incidencia': incidencia})

def mis_incidencias(request):
    
    incidencias = Incidencia.objects.filter(usuario = request.user)
    usuario = request.user.id
    elecciones = Eleccion.objects.filter(usuario_id=usuario, comprado=False)

    context = {
        'incidencias': incidencias,
        'elecciones': elecciones

    }

    return render(request, 'mis_incidencias.html', context)