from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models_dwms import Producto, dwms_guia_headers, dwms_guia_detail

class FormAddProducto(forms.ModelForm):
    inventory_item_id = forms.CharField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"ID inventario", "class":"form-control"} ), label="")
    codigo_producto = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Delfos", "class":"form-control"} ), label="")
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
    search_guia_header = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    folio = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={"placeholder":"Folio guía", "class":"form-control", "name":"folio"}), label="")
    class Meta:
        model = dwms_guia_headers
        fields = ['folio']
        exclude = ("user", )

class FormGuiaDetails(forms.ModelForm):
    pass

