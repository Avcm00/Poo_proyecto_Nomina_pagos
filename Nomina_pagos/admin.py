from django.contrib import admin
from Nomina_pagos.models import Cargo,Departamento,TipoContrato,Rol,Empleado

admin.site.register(Cargo)
admin.site.register(TipoContrato)
admin.site.register(Departamento)
admin.site.register(Rol)
admin.site.register(Empleado)
# Register your models here.
