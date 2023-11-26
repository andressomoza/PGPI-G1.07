from django.shortcuts import render, get_object_or_404
#from cart.forms import CartAddProductForm
from .models import Category, Product, Coche, Accesorio, Eleccion
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect

# from django.views import generic

# class IndexView(generic.ListView):
#     template_name = 'shop/index.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         '''Return five lattest products
#         '''
#         return Product.objects.filter(created__lte=timezone.now()
#         ).order_by('-created')[:5]

def cars_list(request):
    combustible = request.GET.get('combustible', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    tipo_conduccion = request.GET.get('conduccion', '')
    consumo = request.GET.get('consumo', '')
    caballos = request.GET.get('caballos', '')
    cars = Coche.objects.all()
    if combustible:
        cars = cars.filter(combustible=combustible)
    if precio_maximo:
        cars = cars.filter(precio_inicial__lte=precio_maximo)
    if tipo_conduccion:
        cars = cars.filter(conduccion=tipo_conduccion)
    if consumo:
        cars = cars.filter(consumo__lte = consumo)
    if caballos:
        cars = cars.filter(caballos__lte =caballos)
    context = {
        'cars': cars,
        'combustible': combustible,
        'precio_maximo': precio_maximo,
        'conduccion': tipo_conduccion,
        'caballos': caballos,
        'consumo': consumo,
    }

    return render(request, 'shop/cars/list.html', context)

# class ProductListView(generic.ListView):
#     template_name = 'shop/product/list.html'

#     def get_queryset(self):
#         return Product.objects.filter(available=True)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = None
#         if category_slug:
#             category = get_object_or_404(Category, slug=category_slug)
#         context['category'] = category
#         context['categories'] = Category.objects.all()


def car_detail(request, id):
    car = get_object_or_404(Coche, id=id)
    accesorios_disponibles = Accesorio.objects.all()
    if request.method == 'POST' and 'confirmar_eleccion' in request.POST:
        accesorios_seleccionados_ids = request.POST.getlist('accesorios_seleccionados', [])
        accesorios_seleccionados = Accesorio.objects.filter(id__in=accesorios_seleccionados_ids)
    else:
        accesorios_seleccionados = []
        
    if request.method == 'POST' and 'comprar' in request.POST:
        eleccion = Eleccion(coche=car)
        eleccion.save()
        eleccion.accesorios.set(accesorios_seleccionados)
        return HttpResponseRedirect(f'/confirmacion_compra/{eleccion.id}')
    
    precio_total = car.precio_inicial + sum(accesorio.precio for accesorio in accesorios_seleccionados)
    context = {
        'car': car,
        'accesorios_disponibles': accesorios_disponibles,
        'accesorios_seleccionados': accesorios_seleccionados,
        'precio_total': precio_total,
    }
    return render(request, 'shop/cars/detail.html', context)


# class ProductDetialView(generic.DetailView):

#     template_name = 'shop/product/detail.html'
#     model = Product
#     form_class = CartAddProductForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = get_object_or_404(Product, 
#         id=id, slug=slug, available=True)
#         return context