from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    email = models.CharField(max_length=100, verbose_name='Correo electrónico')
    phone = models.CharField(max_length=20, verbose_name='Teléfono')
    degree = models.CharField(max_length=100, verbose_name='Grado')
    school = models.CharField(max_length=50, verbose_name='Escuela')
    university = models.CharField(max_length=100, verbose_name='Universidad')
    sumary = models.TextField(max_length=2000, verbose_name='Resumen')
    previous_work = models.TextField(max_length=2000, verbose_name='Experiencia previa')
    skills = models.CharField(max_length=200, verbose_name='Habilidades')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'