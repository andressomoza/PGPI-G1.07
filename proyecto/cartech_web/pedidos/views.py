from django.shortcuts import render, redirect
from .models import Pedido

'''
def crear_pedido(request):
    if request.method == 'POST':
        form = IncidenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_incidencias')  # Puedes definir esta vista
    else:
        form = IncidenciaForm()

    return render(request, 'incidencias/crear_incidencia.html', {'form': form})
'''

def listar_pedidos(request):
    status = request.GET.get('status', '')
    
    pedidos = Pedido.objects.all()
    if status:
        pedidos = pedidos.filter(status=status)

    context = {
        'pedidos': pedidos,
        'status': status,

    }

    return render(request, 'list.html', context)