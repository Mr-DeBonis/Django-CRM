from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms_dwms import FormAddProducto
from .models_dwms import Producto


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
        print("POST")
        searched = request.POST['searched']
        producto = Producto.objects.filter(codigo_producto__contains=searched).first()
        return render(request, "DWMScodigoBarra.html", {'searched': searched, 'producto': producto})
    else:
        print("NO POST")
        return render(request, "DWMScodigoBarra.html", {})


