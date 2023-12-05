from django.db import models
from user.models import User
import uuid

class Pedido(models.Model):
    class Status(models.TextChoices):
        ENTREGADO = 'entregado', 'Entregado'
        CAMINO = 'camino', 'Camino'
        FABRICACION = 'fabricacion', 'Fabricacion'
    
    class MetodoPago(models.TextChoices):
        CONTRA_REEMBOLSO =  'contra_reembolso', 'Contra reembolso'
        TARJETA =  'tarjeta', 'Tarjeta'

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    nombre = models.CharField(max_length=255, null=True)
    apellidos = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    direccion = models.CharField(max_length=255, null=True)
    ciudad = models.CharField(max_length=100, null=True)
    codigo_postal = models.CharField(max_length=10, null=True)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices, default=MetodoPago.CONTRA_REEMBOLSO)
    status = models.CharField(max_length=11, choices=Status.choices, default=Status.FABRICACION)
    id_pedido = models.CharField(max_length=36, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.id_pedido:
            # Genera un UUID y lo convierte a cadena
            self.id_pedido = str(uuid.uuid4())
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.status}"