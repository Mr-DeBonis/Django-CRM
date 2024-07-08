from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models_dwms import Producto, dwms_guia_headers, dwms_guia_detail

class FormAddProducto(forms.ModelForm):
    inventory_item_id    = forms.CharField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"ID inventario", "class":"form-control"} ), label="")
    codigo_producto      = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Delfos", "class":"form-control"} ), label="")
    descripcion_producto = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Descripción", "class":"form-control"} ), label="")

    class Meta:
        model = Producto
        exclude = ("user", )


class FormSearchProducto(forms.ModelForm):
    codigo_producto = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Delfos", "class":"form-control"} ), label="")

    class Meta:
        model = Producto
        exclude = ("user", )


class FormGuiaHeader(forms.ModelForm):
    folio = forms.IntegerField(
        required = False,
        widget=forms.widgets.NumberInput(attrs={
            "placeholder":"Folio guía", 
            "class":"form-control mb-9", 
            "name":"folio", 
            "required min":"1"}), label="")
    class Meta:
        model = dwms_guia_headers
        fields = ['folio']
        exclude = ("user", )


class FormCodigoBarrasCantidad(forms.Form):
    codigo_barra = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(attrs={
            "placeholder":"Código de barras", 
            "class":"form-control"}), 
            label="Código de barras")
    
    cantidad_producto = forms.IntegerField(
        required=False,
        initial=1,
        widget=forms.widgets.NumberInput(attrs={
            "placeholder":"Cantidad escaneada", 
            "class":"form-control",  
            "required min":"1"}), 
            label="Cantidad")
    
    def __init__(self, *args, **kwargs):
        super(FormCodigoBarrasCantidad, self).__init__(*args, **kwargs)
        self.fields['codigo_barra'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Código de Barra'})
        self.fields['cantidad_producto'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cantidad escaneada'})


class FormEmpaquetado(forms.ModelForm):
    peso = forms.IntegerField(
        required = True,
        initial=1,
        widget = forms.widgets.NumberInput(attrs={
            'placeholder' : 'Peso (gramos)',
            "class":"form-control",
            "required min" : "1",
            'id':"pesoEmpaquetado"
        }), label="Peso del bulto")
    
    cantidad_bultos = forms.IntegerField(
        required = True,
        initial=1,
        widget = forms.widgets.NumberInput(attrs={
            'placeholder':'Cantidad de Bultos',
            "class":"form-control",
            "required min" : "1",
            "id" : "cantidad_bultos"
        }), label="Cantidad de bultos")
    
    class Meta:
        model = dwms_guia_headers
        fields = ['peso', 'cantidad_bultos']
        exclude = ("user", )
