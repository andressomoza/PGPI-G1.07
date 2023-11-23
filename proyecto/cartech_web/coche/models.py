from django.db import models

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
    
    accesorios = models.ManyToManyField('Accesorios', related_name='coches')
    
    def get_precio_total(self):
        total_coste_accesorios = self.accesorios.aggregate(total=models.Sum('precio'))['total'] or 0
        return self.precio_inicial + total_coste_accesorios
    
class Accesorios(models.Model):
    
    precio = models.IntegerField()
    nombre = models.CharField(max_length=50)

class Usuario(models.Model):
    
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)

