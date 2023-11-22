from django import forms
import datetime
from .models import Reserva,estadoReserva,tipoReserva

class reservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
    
    ESTADOS_CHOICES = (
        {"guardado","GUARDADO"},
        {"anulado","ANULADO"},
        {"confirmado","CONFIRMADO"}
    )
    
    fechareserva = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}),
        input_formats=['%Y-%m-%d'],
        label='Fecha Reserva'
    )
    horareserva = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type':'time','format':'%H:%M'}),label='Hora Reserva')
    observaciones = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':4,'cols':50}))
    cantidadHermanos = forms.IntegerField(label='Cantidad de Hermanos')
    
    estadoReservaId = forms.ModelChoiceField(queryset=estadoReserva.objects.all(),label="Estado Reserva")
    estadoReservaId.widget.attrs['class'] = 'form-select'
    
    tipoSolicitudId = forms.ModelChoiceField(queryset=tipoReserva.objects.all(),label='Tipo Reserva')
    tipoSolicitudId.widget.attrs['class'] = 'form-select'
    
    imagenCarnet = forms.ImageField(widget=forms.ClearableFileInput,label="Foto Carnet")
    imagenCarnet.widget.attrs['class'] = 'custom-file-input'
    
    fchNacimiento = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}),
        input_formats=['%Y-%m-%d'],
        label='Fecha Nacimiento'
    )
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) <= 2:
            raise forms.ValidationError("El nombre debe tener mas de 2 letras.")
        return nombre
    
    def clean_observaciones(self):
        observaciones = self.cleaned_data.get('observaciones')
        palabras = observaciones.split()
        
        if len(palabras) <5:
            raise forms.ValidationError("Las observaciones deben contener al menos 5 palabras.")
        
        return observaciones
    