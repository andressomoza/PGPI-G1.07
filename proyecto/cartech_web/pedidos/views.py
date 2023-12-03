from django.shortcuts import get_object_or_404, render
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

    return render(request, 'listar_pedidos.html', context)

def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario = request.user)

    context = {
        'pedidos': pedidos,
    }

    return render(request, 'mis_pedidos.html', context)

def detalle_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    coche = pedido.eleccion.coche
    accesorios = []
    precio_total = pedido.eleccion.get_precio_total
    if pedido.eleccion.accesorios:
        for accesorio in pedido.eleccion.accesorios:
            accesorios.append(accesorio)
    context = {
        'pedido': pedido,
        'coche':coche,
        'accesorios': accesorios,
        'precio_total':precio_total

    }
    return render(request, 'detalle_pedido.html', context)