from django.db import models
from django.urls import reverse
from shop.models import Eleccion
from django.contrib.auth.models import User
import uuid

class Pedido(models.Model):
    class Status(models.TextChoices):
        ENTREGADO = 'entregado', 'Entregado'
        CAMINO = 'camino', 'Camino'
        FABRICACION = 'fabricacion', 'Fabricacion'

    eleccion = models.ForeignKey(Eleccion, related_name='pedido', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=Status.choices, default=Status.FABRICACION)
    id_pedido = models.CharField(max_length=36, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.id_pedido:
            # Genera un UUID y lo convierte a cadena
            self.id_pedido = str(uuid.uuid4())
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.status}"