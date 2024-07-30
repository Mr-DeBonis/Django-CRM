from django.contrib import admin
from .models import Record
from .models_dwms import dwms_guia_header, dwms_guia_detail, dwms_codigo_barra, dwms_comuna, dwms_zona, Producto

admin.site.register(Record)
admin.site.register(dwms_guia_header)
admin.site.register(dwms_guia_detail)
admin.site.register(dwms_codigo_barra)
admin.site.register(dwms_comuna)
admin.site.register(dwms_zona)
admin.site.register(Producto)
