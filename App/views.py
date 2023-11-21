from django.shortcuts import render,redirect

from .models import Reserva
from .forms import reservaForm

# Create your views here.
def agregarReserva(request):
    form = reservaForm()
    if request.method == 'POST':
        form = reservaForm(request.POST)
        if form.is_valid():
            form.save()
            form = reservaForm()
    
    reservas = Reserva.objects.all()
    data = {'form':form,'reservas':reservas}
    return render(request,'templatesApp/agregar.html',data)

def eliminarReserva(request,id):
    reserva = Reserva.objects.get(idSolicitud=id)
    reserva.delete()
    return redirect('/')

def actualizarReserva(request,id):
    reserva = Reserva.objects.get(idSolicitud=id)
    form = reservaForm(instance=reserva)
    if (request.method == 'POST'):
        form = reservaForm(request.POST,instance=reserva)
        if form.is_valid():
            form.save()
            form = reservaForm()
            
    reservas = Reserva.objects.all()
    data = {'form':form,'reservas':reservas}
    return render(request,'templatesApp/agregar.html',data)