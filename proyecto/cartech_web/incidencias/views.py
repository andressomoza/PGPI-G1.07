from django.shortcuts import render, redirect
from .forms import IncidenciaForm
from .models import Incidencia

def crear_incidencia(request):
    if request.method == 'POST':
        form = IncidenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_incidencias')  # Puedes definir esta vista
    else:
        form = IncidenciaForm()

    return render(request, 'incidencias/crear_incidencia.html', {'form': form})


def incidencias_list(request):
    urgencia = request.GET.get('urgencia', '')
    
    incidencias = Incidencia.objects.all()
    if urgencia:
        incidencias = incidencias.filter(urgencia=urgencia)

    context = {
        'incidencias': incidencias,
        'urgencia': urgencia,

    }

    return render(request, 'incidencias/list.html', context)