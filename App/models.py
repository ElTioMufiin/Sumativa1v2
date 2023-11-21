
from django.db import models

# Create your models here.
class estadoReserva(models.Model):
    
    estadoReservaId = models.CharField(primary_key=True,max_length=3)
    estadoReservaNombre = models.CharField(max_length=20)
    
    def __str__(self):
        return "{}".format(self.estadoReservaNombre)
    
class tipoReserva(models.Model):
    
    tipoSolicitudId = models.CharField(primary_key=True, max_length=3)
    tipoSolicitud = models.CharField( max_length=20)
    
    def __str__(self):
        return "{}".format(self.tipoSolicitud)
    
    
class Reserva(models.Model):
    
    idSolicitud = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=12)
    fechareserva = models.DateField()
    horareserva = models.TimeField()
    cantidadpersonas = models.IntegerField()
    
    observaciones = models.CharField(max_length=5000)
    
    website = models.URLField()
    email = models.EmailField()
    donate = models.BooleanField()
    edad = models.IntegerField()
    
    estadoReservaId = models.ForeignKey(estadoReserva,null=True,blank=False,on_delete=models.RESTRICT)
    tipoSolicitudId = models.ForeignKey(tipoReserva,null=True,blank=False,on_delete=models.RESTRICT)
        