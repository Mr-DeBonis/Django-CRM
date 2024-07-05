from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms_dwms import FormAddProducto, FormGuiaHeader, FormCodigoBarrasCantidad, FormEmpaquetado
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
            return render(request, "DWMScodigoBarra.html", {'searched': codigo_producto, 'producto': producto, 'codigos_barra': codigos_barra})

    else:
        return render(request, "DWMScodigoBarra.html", {})


def DWMSrevisionPicking(request, folio = ''):
    form_guia = FormGuiaHeader(request.POST or None)
    form_codigo_barras_cantidad = FormCodigoBarrasCantidad(request.POST or None)
    guia_details = []
    

    if request.method == "POST":
        folio = request.POST.get("folio", False)
        codigo_barra = request.POST.get("codigo_barra", False)
        cantidad_producto = request.POST.get("cantidad_producto", False)

        if folio:
            try:
                print("folio: " + str(folio))
                guia_header = dwms_guia_headers.objects.get(folio=folio)
                guia_details = dwms_guia_detail.objects.filter(header=guia_header).select_related()
            except dwms_guia_headers.DoesNotExist:
                messages.error(request, "No se ha encontrado el folio")

        if codigo_barra:
            # Obtener producto y cantidad asociada al codigo de barras.
            # Marcar guia_detai lcomo revisado, indicar datetime y estado de revision
            try:
                barcode =  dwms_codigo_barra.objects.get(codigo=codigo_barra)
                guia_detail = dwms_guia_detail.objects.filter(
                    header=guia_header,
                    producto=barcode.producto).get()

                print(guia_detail.revisado)
                
                cantidad_producto = int(cantidad_producto) * barcode.cantidad
                print(type(cantidad_producto))
                print(type(guia_detail.cantidad_producto))

                if cantidad_producto == guia_detail.cantidad_producto:
                    print("Cantidades iguales")
                    guia_detail.revisado = True
                    guia_detail.fecha_revision = timezone.make_aware(datetime.now())
                    guia_detail.save()
            except dwms_guia_detail.DoesNotExist:
                messages.error(request, "Este producto no está en la guía")



    context = {
        'form_guia' : form_guia,
        'form_codigo_barras_cantidad' : form_codigo_barras_cantidad,
        'guia_details' : guia_details,
        'folio': folio
    }

    return render(request, "DWMSrevisionPicking.html", context=context)


def DWMSLlamarSupervisor(request, pk):
    guia_header = dwms_guia_headers.objects.get(folio=pk)
    guia_details = dwms_guia_detail.objects.filter(header=guia_header).select_related()

    context = {
        'folio' : pk,
        'guia_details' : guia_details
    }


    return render(request, "DWMSLlamarSupervisor.html", context=context)


def DWMSEmpaquetado(request, pk):
    form_empaquetado = FormEmpaquetado(request.POST or None)
    peso = request.POST.get("peso", False)
    if peso:
        guia_header = dwms_guia_headers.objects.get(folio=pk)

        guia_header.peso = request.POST.get("peso")
        guia_header.cantidad_bultos = request.POST.get("cantidad_bultos")
        guia_header.etiquetado = True
        guia_header.revisado = True
        guia_header.fecha_revision = timezone.make_aware(datetime.now())
        guia_header.user = request.user

        guia_header.save()

        return redirect("DWMSrevisionPicking")

    context = {
        'form_empaquetado': form_empaquetado
    }
    return render(request, "DWMSEmpaquetado.html", context=context)

