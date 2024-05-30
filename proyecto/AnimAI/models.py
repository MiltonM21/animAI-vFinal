from django.db import models

class MiModelo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'AnimAI'
    def __str__(self):
        return self.nombre


