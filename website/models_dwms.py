from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class dwms_guia_headers(models.Model):
    # TODO: CAMBIAR NOMBRE A SINGULAR; NO PLURAL
    folio              = models.IntegerField(blank=True, null=True, verbose_name='Folio')
    peso               = models.IntegerField(blank=True, null=True, verbose_name='Peso (gramos)')
    cantidad_bultos    = models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Bultos')
    etiquetado         = models.BooleanField(default=False, verbose_name='Etiquetado')
    revisado           = models.BooleanField(default=False, verbose_name='Revisado')
    fecha_creacion     = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Fecha de Creacion')
    fecha_revision     = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Revision')
    rut_receptor       = models.CharField(max_length=1000, blank=True, null=True, verbose_name='RUT')
    razon_soc_receptor = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Cliente')
    dir_receptor       = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Direccion')
    hh                 = models.CharField(max_length=1000, blank=True, null=True, verbose_name='HH')
    comuna_receptor    = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Comuna')
    ciudad_receptor    = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Ciudad')
    region_receptor    = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Region')
    instr_envio        = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Instrucciones de Envio')
    contacto           = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Contacto')
    trx_number         = models.IntegerField(blank=True, null=True, verbose_name='TRX_NUMBER')
    comuna             = models.ForeignKey('dwms_comuna', blank=True, null=True, on_delete=models.DO_NOTHING)
    user               = models.ForeignKey(User, blank=True, null=True, verbose_name='Usuario', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Guia'
        verbose_name_plural = 'Guias'

class dwms_guia_detail(models.Model):
    header            = models.ForeignKey('dwms_guia_headers', blank=True, null=True, on_delete=models.DO_NOTHING)
    producto          = models.ForeignKey('Producto', blank=True, null=True, on_delete=models.DO_NOTHING)
    fecha_revision    = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Revision') # Añadir auto_now = True
    revisado          = models.BooleanField(default=False, verbose_name='Revisado')
    cantidad_producto = models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Productos')

    class Meta:
        verbose_name = 'Linea'
        verbose_name_plural = 'Lineas'

class dwms_codigo_barra(models.Model):
    # TODO Marcar codigo como único
    producto           = models.ForeignKey('Producto', blank=True, null=True, on_delete=models.DO_NOTHING)
    codigo             = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Codigo')
    cantidad           = models.IntegerField(blank=True, null=True, verbose_name='Cantidad')
    fecha_creacion     = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Fecha de Creacion')
    fecha_modificacion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Modificacion')
    creacion_user      = models.ForeignKey(User, blank=True, null=True, verbose_name='Usuario de Creacion', on_delete=models.DO_NOTHING, related_name='creacion_user')
    mod_user           = models.ForeignKey(User, blank=True, null=True, verbose_name='Usuario de Modificacion', on_delete=models.DO_NOTHING, related_name='mod_user')

    class Meta:
        verbose_name = 'Codigo'
        verbose_name_plural = 'Codigos'

class dwms_comuna(models.Model):
    nombre = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Comuna')
    zona   = models.ForeignKey('dwms_zona', blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'

class dwms_zona(models.Model):
    nombre      = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Zona')
    observacion = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Observacion')

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'



class Producto(models.Model):
    inventory_item_id = models.PositiveIntegerField()
    codigo_producto = models.CharField(max_length=50)
    descripcion_producto = models.CharField(max_length=240)

    class Meta:
        ordering = ["-descripcion_producto"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    def __str__ (self):
        return "{0} - {1}".format(self.codigo_producto, self.descripcion_producto)