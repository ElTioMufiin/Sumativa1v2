from django.shortcuts import render,redirect
#PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from django.http import FileResponse
import io
#PDF
#QR
import qrcode
#QR
import base64
from .models import Reserva
from .forms import reservaForm

# Create your views here.
def agregarReserva(request):
    form = reservaForm()
    if request.method == 'POST':
        form = reservaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            reserva = Reserva.objects.latest('idSolicitud')
            reserva.codigoQr = generarQR(reserva)
            reserva.save()
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
            reserva.codigoQr = generarQR(reserva)
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
    
    page_width, page_height = letter
    print(f"Page Height: {page_height}")
    print(f"Page Height: {page_width}")
    
    
    ancho = 400
    alto = 200
    x = 20
    y = 608
    
    t.wrapOn(pdf,ancho,alto)
    t.drawOn(pdf,x,y)
    
    fotox = x+t._width+50
    fotoy = y
    
    carnet = ImageReader(reserva.imagenCarnet)
    pdf.drawString(fotox+19,742,"Foto Carnet")
    pdf.drawImage(carnet, fotox, fotoy , width=100, height=128, mask=None)
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    

    
    response = FileResponse(buffer,as_attachment=False,filename=f'media/pdf/{reserva.idSolicitud}.pdf',content_type='application/pdf')
    
    return response

def generarPDFQR(request,id):
    
    reserva = Reserva.objects.get(idSolicitud=id)
    qr = reserva.codigoQr
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
    
    page_width, page_height = letter
    print(f"Page Height: {page_height}")
    print(f"Page Height: {page_width}")
    
    
    ancho = 400
    alto = 200
    x = 20
    y = 608
    
    t.wrapOn(pdf,ancho,alto)
    t.drawOn(pdf,x,y)
    
    fotox = x+t._width+50
    fotoy = y
    
    carnet = ImageReader(reserva.imagenCarnet)
    pdf.drawString(fotox+19,742,"Foto Carnet")
    pdf.drawImage(carnet, fotox, fotoy , width=100, height=128, mask=None)
    qrImg = ImageReader(io.BytesIO(base64.b64decode(qr)))
    pdf.drawImage(qrImg, 200, y-260, width=200, height=200, mask=None)
    
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    

    
    response = FileResponse(buffer,as_attachment=False,filename=f'media/pdf/{reserva.idSolicitud}.pdf',content_type='application/pdf')
    
    return response

def generarQR(reserva):
    ##Variables para crear QR
    rNom = f'Nombre :{reserva.nombre}.'
    edad = f'Edad :{reserva.edad()}'
    rTel = f'Telefono :{reserva.telefono}.'
    rFchR = f'Fecha Reserva : {reserva.fechareserva}.'
    rHrR = f'Hora Reserva : {reserva.horareserva}.'
    rObs = f'Observaciones : {reserva.observaciones}.'
    rEst = f'Estado : {reserva.estadoReservaId}.'
    ##Pasar Variables al QR
    qr= qrcode.make(f'{rNom}\n{edad}\n{rTel}\n{rFchR}\n{rHrR}\n{rObs}\n{rEst}')
    ##Crear Buffer,guardar QR al buffer y leer desde el buffer
    buffer = io.BytesIO()
    qr.save(buffer)
    buffer.seek(0)
    ##Codificar la imagen a base64
    img = base64.b64encode(buffer.read()).decode('utf-8')
    
    return img

def mostrarQR(request,id):
    #Buscar Reserva con su ID
    reserva = Reserva.objects.get(idSolicitud=id)
    buffer = io.BytesIO()
    qr = reserva.codigoQr
    
    pdf = canvas.Canvas(buffer,pagesize=letter)
    pdf.setTitle(f"QR Reserva {reserva.idSolicitud}")
    #Decodificar Base64 para recuperar la imagen
    qrImg = ImageReader(io.BytesIO(base64.b64decode(qr)))
    pdf.drawImage(qrImg, 200, 550, width=200, height=200, mask=None)
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    
    response = FileResponse(buffer,as_attachment=False,content_type='application/pdf')
    
    return response
