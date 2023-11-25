from django.db import models
from django.urls import reverse

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
    
    accesorios = models.ManyToManyField(Accesorio, related_name='coches',blank=True)
    
    def get_precio_total(self):
        total_coste_accesorios = self.accesorios.aggregate(total=models.Sum('precio'))['total'] or 0
        return self.precio_inicial + total_coste_accesorios

    def get_absolute_url(self):
        return reverse('shop:car_detail', args=[self.id])

class Usuario(models.Model):
    
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)
    
    class Meta:
        app_label = 'usuario'
        
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
