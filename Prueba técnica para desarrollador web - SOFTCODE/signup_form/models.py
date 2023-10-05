from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=25)
    apellido = models.CharField(null=False, max_length=25)
    email = models.CharField(null=False, max_length=100)
    password = models.CharField(null=False, max_length=256)

    def __str__(self):
        return self.nombre
