from django.shortcuts import render, redirect ,get_object_or_404
from .forms import OpinionForm
from .models import Opinion
from django.contrib.auth.decorators import user_passes_test
from cartech_web.views import is_admin
from django.http import HttpResponseRedirect

def pagina_base(request):
    return render(request, 'base.html')

def crear_opinion(request):
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.usuario = request.user 
            opinion.save()
            return HttpResponseRedirect('/opiniones/me')
    else:
        form = OpinionForm()

    return render(request, 'crear_opinion.html', {'form': form})

@user_passes_test(is_admin)
def listar_opiniones(request):
    valoracion = request.GET.get('valoracion', '')
    
    opiniones = Opinion.objects.all()
    if valoracion:
        opiniones = opiniones.filter(valoracion=valoracion)

    context = {
        'opiniones': opiniones,
        'valoracion': valoracion,

    }

    return render(request, 'listar_opiniones.html', context)

@user_passes_test(is_admin)
def borrar_opinion(request, id):
    opinion = get_object_or_404(Opinion, id=id)

    if request.method == 'POST':
        opinion.delete()
        return HttpResponseRedirect('/opiniones/list')  

    return render(request, 'borrar_opinion.html', {'opinion': opinion})

def mis_opiniones(request):
    
    opiniones = Opinion.objects.filter(usuario = request.user)

    context = {
        'opiniones': opiniones,
    }

    return render(request, 'mis_opiniones.html', context)