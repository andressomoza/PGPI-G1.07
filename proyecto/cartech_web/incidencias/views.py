from django.shortcuts import render, redirect ,get_object_or_404
from .forms import IncidenciaForm
from .models import Incidencia
from django.contrib.auth.decorators import user_passes_test
from cartech_web.views import is_admin
from django.http import HttpResponseRedirect

def pagina_base(request):
    return render(request, 'base.html')

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

    return render(request, 'crear_incidencia.html', {'form': form})

@user_passes_test(is_admin)
def listar_incidencias(request):
    urgencia = request.GET.get('urgencia', '')
    
    incidencias = Incidencia.objects.all()
    if urgencia:
        incidencias = incidencias.filter(urgencia=urgencia)

    context = {
        'incidencias': incidencias,
        'urgencia': urgencia,

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

    context = {
        'incidencias': incidencias,

    }

    return render(request, 'mis_incidencias.html', context)