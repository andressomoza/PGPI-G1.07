from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, Group
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class MetodoPago(models.TextChoices):
        CONTRA_REEMBOLSO =  'contra_reembolso', 'Contra reembolso'
        TARJETA =  'tarjeta', 'Tarjeta'
    
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, null=True)
    ciudad = models.CharField(max_length=100, null=True)
    codigo_postal = models.CharField(max_length=10, null=True)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices, default=MetodoPago.CONTRA_REEMBOLSO)
    
    # Otros campos y métodos personalizados

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return self.username

User.groups.field.remote_field.related_name = "user_groups"
User.user_permissions.field.remote_field.related_name = "user_permissions"