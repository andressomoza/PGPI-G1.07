from django.db import models
from django.urls import reverse
from shop.models import Eleccion

class Pedido(models.Model):
    class Status(models.TextChoices):
        ENTREGADO = 'entregado', 'Entregado'
        CAMINO = 'camino', 'Camino'
        FABRICACION = 'fabricacion', 'Fabricacion'

    eleccion = models.ForeignKey(Eleccion, related_name='pedido', on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=Status.choices, default=Status.FABRICACION)

    def __str__(self):
        return f"{self.status}"