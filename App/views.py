from django.shortcuts import render,redirect

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from django.http import FileResponse
import io

from .models import Reserva
from .forms import reservaForm

# Create your views here.
def agregarReserva(request):
    form = reservaForm()
    if request.method == 'POST':
        form = reservaForm(request.POST, request.FILES)
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

def crearPDF(request,id):
    
    reserva = Reserva.objects.get(idSolicitud=id)
    
    buffer = io.BytesIO()
    
    pdf = canvas.Canvas(buffer,pagesize=letter)
    pdf.setTitle(f"Resumen Reserva{reserva.idSolicitud}")
    
    data_pdf =  [['Solicitud de Reserva','Datos']]
    
    resultado = reserva.edad()

    data_pdf.append(['Nombre', reserva.nombre])
    data_pdf.append(['Fecha Reserva', f"{reserva.fchCreacion}"])
    data_pdf.append(['Telefono', reserva.telefono])
    data_pdf.append(['Website', reserva.website])
    data_pdf.append(['Edad', resultado])
    data_pdf.append(['Email', reserva.email])
    data_pdf.append(['Fecha Nacimiento', f"{reserva.fchNacimiento}"])
    
    t = Table(data_pdf, style=[('GRID',(0,0),(-1,-1),(0-5),colors.grey)])
    
    ancho = 400
    alto = 200
    x = 10
    y = 200
    
    t.wrapOn(pdf,ancho,alto)
    t.drawOn(pdf,x,y)
    
    carnet = ImageReader(reserva.imagenCarnet)
    pdf.drawString(50,180,"Foto Carnet")
    pdf.drawImage(carnet, 140, 90, width=128, height=102.4, mask=None)
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    
    response = FileResponse(buffer,as_attachment=False,filename=f'media/pdf/{reserva.idSolicitud}.pdf',content_type='application/pdf')
    
    return response
    