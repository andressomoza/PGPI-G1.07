from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Accesorio(models.Model):
    
    precio = models.IntegerField()
    nombre = models.CharField(max_length=50)
        
class Coche(models.Model):
    
    class Combustible(models.TextChoices):
        GASOLINA = 'gasolina', 'Gasolina'
        DIESEL = 'diesel', 'Diesel'
        HIBRIDO = 'hibrido', 'Hibrido'
        ELECTRICO = 'electrico', 'Electrico'
        
    class Conduccion(models.TextChoices):
        MANUAL = 'manual', 'Manual'
        AUTOMATICO = 'automatico', 'Automatico'
    
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    combustible = models.CharField(max_length=20, choices=Combustible.choices, default=Combustible.GASOLINA)
    conduccion = models.CharField(max_length=20, choices=Conduccion.choices, default=Conduccion.MANUAL)
    consumo = models.FloatField()
    caballos = models.IntegerField()
    precio_inicial = models.IntegerField()
    
    def get_absolute_url(self):
        return reverse('shop:car_detail', args=[self.id])
    
        
class Eleccion(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    coche = models.ForeignKey(Coche, related_name='elecciones', on_delete=models.CASCADE)
    accesorios = models.ManyToManyField(Accesorio, related_name='elecciones',blank=True)
    
    def get_precio_total(self):
        precio_base = self.coche.precio_inicial
        total_coste_accesorios = self.accesorios.aggregate(total=models.Sum('precio'))['total'] or 0
        return precio_base + total_coste_accesorios
    
    def get_absolute_url(self):
        return reverse('pedidos:detalle_pedido', args=[self.id])
    
        
