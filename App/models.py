from collections.abc import Iterable
from django.db import models
import datetime

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
    cantidadHermanos = models.IntegerField()
    
    observaciones = models.CharField(max_length=5000)
    
    website = models.URLField()
    email = models.EmailField()
    donate = models.BooleanField()
    fchNacimiento = models.DateField()
    
    estadoReservaId = models.ForeignKey(estadoReserva,null=True,blank=False,on_delete=models.RESTRICT)
    tipoSolicitudId = models.ForeignKey(tipoReserva,null=True,blank=False,on_delete=models.RESTRICT)
    
    imagenCarnet = models.ImageField(upload_to="carnets/")
    fchCreacion = models.DateTimeField(auto_now_add=True)
    fchModificacion = models.DateTimeField(auto_now=True)
    # codigoQr = models.ImageField(upload_to='codigoqr/')
    
    def edad(self):
        hoy = datetime.datetime.now().date()
        nac = self.fchNacimiento
        edad = hoy.year - nac.year - ((hoy.month, hoy.day) < (nac.month, nac.day))
        return int(edad)
    
    