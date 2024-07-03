from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms_dwms import FormAddProducto, FormGuiaHeader
from .models_dwms import Producto, dwms_codigo_barra, dwms_guia_headers, dwms_guia_detail


def producto(request):
    productos = Producto.objects.all()

    return render(request, "producto.html", {'productos': productos})


def add_producto(request):
    form = FormAddProducto(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_producto = form.save()
                messages.success(request, "Producto añadido!")
                return redirect("producto")
        return render(request, "add_producto.html", {"form": form})
    else:
        messages.success(request, "You must be logged in to see this page")
        return redirect('producto')


def DWMScodigoBarra(request):
    if request.method == "POST":
        if 'searched' in request.POST:
            codigo_producto  = request.POST.get('searched', False)
            producto = Producto.objects.filter(codigo_producto__contains=codigo_producto ).first()
            codigos_barra = dwms_codigo_barra.objects.filter(producto = producto).select_related()
            return render(request, "DWMScodigoBarra.html", {'searched': codigo_producto , 'producto': producto, 'codigos_barra' : codigos_barra})
        elif 'codigo_barra' in request.POST and 'producto_id' in request.POST:
            codigo_barra = request.POST.get('codigo_barra', False)
            cantidad = request.POST.get('cantidad', False)
            producto_id = request.POST.get('producto_id', False)
            producto = get_object_or_404(Producto, id=producto_id)
            codigo_producto = producto.codigo_producto
            codigos_barra = dwms_codigo_barra.objects.filter(producto=producto)


            if codigo_barra and cantidad:
                dwms_codigo_barra.objects.create(
                    producto=producto,
                    codigo=codigo_barra,
                    cantidad=cantidad,
                    creacion_user=request.user,
                    mod_user=request.user,
                    fecha_creacion=timezone.now(),
                    fecha_modificacion=timezone.now()
                )
            return render(request, "DWMScodigoBarra.html", {'searched': codigo_producto , 'producto': producto, 'codigos_barra' : codigos_barra})
            
    else:
        return render(request, "DWMScodigoBarra.html", {})


def DWMSrevisionPicking(request):
    form_guia = FormGuiaHeader(request.POST or None)
    header_id = None
    if request.method == "POST":
        if 'folio' in request.POST:
            if form_guia.is_valid():
                folio = form_guia.cleaned_data.get('folio')
                try:
                    guia_header = dwms_guia_headers.objects.get(folio=folio)
                    header_id = guia_header.id
                except dwms_guia_headers.DoesNotExist:
                    messages.error(request, "No se ha encontrado el folio")
                    return render(request, "DWMSrevisionPicking.html", {"form_guia":form_guia})
            else:
                print("Form is not valid")
        else:
            print('No form_guia')
    return render(request, "DWMSrevisionPicking.html", {"form_guia":form_guia})
