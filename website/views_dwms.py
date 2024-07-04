from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms_dwms import FormAddProducto, FormGuiaHeader, FormCodigoBarrasCantidad
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


def DWMSrevisionPicking(request):
    form_guia = FormGuiaHeader(request.POST or None)
    form_codigo_barras_cantidad = FormCodigoBarrasCantidad(request.POST or None)
    guia_details = []
    folio = ''

    if request.method == "POST":
        folio = request.POST.get("folio", False)
        if folio:
            try:
                print("folio: " + str(folio))
                guia_header = dwms_guia_headers.objects.get(folio=folio)
                guia_details = dwms_guia_detail.objects.filter(header=guia_header).select_related()
            except dwms_guia_headers.DoesNotExist:
                messages.error(request, "No se ha encontrado el folio")

        codigo_barra = request.POST.get("codigo_barra", False)
        if codigo_barra:
            try:
                guia_details = dwms_guia_detail.objects.filter(header=guia_header).select_related()
            except: 
                pass


    context = {
        'form_guia' : form_guia,
        'form_codigo_barras_cantidad' : form_codigo_barras_cantidad,
        'guia_details' : guia_details,
        'folio': folio
    }

    return render(request, "DWMSrevisionPicking.html", context=context)
