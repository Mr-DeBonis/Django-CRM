from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models_dwms import Producto

class FormAddProducto(forms.ModelForm):
    inventory_item_id = forms.CharField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"ID inventario", "class":"form-control"} ), label="")
    codigo_producto = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Delfos", "class":"form-control"} ), label="")
    descripcion_producto = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Descripción", "class":"form-control"} ), label="")

    class Meta:
        model = Producto
        exclude = ("user", )
