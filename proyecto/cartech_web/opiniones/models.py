from django.db import models
from django.urls import reverse
from user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Opinion(models.Model):
    ESTRELLAS_CHOICES = [
        (1, 'Una estrella'),
        (2, 'Dos estrellas'),
        (3, 'Tres estrellas'),
        (4, 'Cuatro estrellas'),
        (5, 'Cinco estrellas'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    valoracion = models.IntegerField(choices=ESTRELLAS_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])

    fecha_creacion = models.DateTimeField(auto_now_add=True)



