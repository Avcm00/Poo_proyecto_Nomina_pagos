from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Empleado, Departamento, Cargo, TipoContrato, Rol


def login(request):
    form = UserCreationForm
    
    if request.method == 'GET':
        return render(request, 'login/login.html', {"form": form})
    else:
        # Verificamos si el formulario enviado es de registro o inicio de sesión
        form_type = request.POST.get('form_type', '')
        
        if form_type == 'register':
            # Lógica para el registro
            if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = User.objects.create_user(
                        request.POST["username"], 
                        password=request.POST["password1"]
                    )
                    user.save()
                    auth_login(request, user)
                except IntegrityError:
                    return render(request, 'login/login.html', {
                        "form": form, 
                        "error": "El nombre de usuario ya existe.",
                        "active_tab": "register"  
                    })
            return render(request, 'login/login.html', {
                "form": form, 
                "error": "Las contraseñas no coinciden.",
                "active_tab": "register"  
            })
        else:
            # Lógica para el inicio de sesión
            user = authenticate(
                request, 
                username=request.POST['username'], 
                password=request.POST['password']
            )
            if user is None:
                return render(request, 'login/login.html', {
                    "form": form, 
                    "error": "El nombre de usuario o la contraseña son incorrectos.",
                    "active_tab": "login"  # Para mantener la pestaña de login activa
                })
            
            auth_login(request, user)
            return redirect('index')
  
def index(request):
    empleados = Empleado.objects.count()
    departamento = Departamento.objects.count()
    roles = Rol.objects.count()
    contrato = TipoContrato.objects.count()
      
      
    data = {
        'empleados': empleados,
        'departamento': departamento,
        'contrato': contrato,
        'roles': roles,
        'data_empleado': Empleado,
        'data_departamento': Departamento,
        'data_cargo': Cargo,
        'data_tipo_contrato': TipoContrato,
        'data_rol': Rol,
    }
    
    
    return render(request, "index.html", data)


def listar_modelo(request, modelo=None):
    # Diccionario que mapea nombres de modelos a las clases correspondientes
    modelos = {
        'empleado': Empleado,
        'departamento': Departamento,
        'cargo': Cargo,
        'tipo_contrato': TipoContrato,
        'rol': Rol,
    }
    
    # Diccionario para títulos personalizados
    titulos = {
        'empleado': 'Listado de Empleados',
        'departamento': 'Listado de Departamentos',
        'cargo': 'Listado de Cargos',
        'tipo_contrato': 'Listado de Tipos de Contrato',
        'rol': 'Listado de Roles de Pago',
    }
    
    # Si no se especifica un modelo o el modelo no existe, redirigir al inicio
    if not modelo or modelo not in modelos:
        messages.error(request, "Modelo no válido")
        return redirect('index')
    
    # Obtener el modelo seleccionado
    modelo_seleccionado = modelos[modelo]
    
    # Obtener los objetos del modelo
    objetos = modelo_seleccionado.objects.all()
    
    # Preparar el contexto para la plantilla
    contexto = {
        'objetos': objetos,
        'titulo': titulos[modelo],
        'modelo': modelo,
    }
    
    return render(request, "modelo/listado_modelos.html", contexto)

def detalle_modelo(request, modelo=None, id=None):

    modelos = {
        'empleado': Empleado,
        'departamento': Departamento,
        'cargo': Cargo,
        'tipo_contrato': TipoContrato,
        'rol': Rol,
    }
    
    if not modelo or modelo not in modelos or not id:
        messages.error(request, "Modelo o ID no válido")
        return redirect('index')
    
    modelo_seleccionado = modelos[modelo]
    
    objeto = get_object_or_404(modelo_seleccionado, pk=id)
    
    contexto = {
        'objeto': objeto,
        'modelo': modelo,
    }
    
    return render(request, "modelo/detalle_modelo.html", contexto)

def formulario_modelo(request, modelo=None, id=None):
    modelos = {
        'empleado': Empleado,
        'departamento': Departamento,
        'cargo': Cargo,
        'tipo_contrato': TipoContrato,
        'rol': Rol,
    }
    
    if not modelo or modelo not in modelos:
        messages.error(request, "Modelo no válido")
        return redirect('index')

    modelo_seleccionado = modelos[modelo]
    objeto = None
    accion = "Crear"
    if id:
        objeto = get_object_or_404(modelo_seleccionado, pk=id)
        accion = "Editar"
    contexto = {
        'objeto': objeto,
        'modelo': modelo,
        'accion': accion,
    }
    if modelo == 'empleado':
        contexto['departamentos'] = Departamento.objects.all()
        contexto['cargos'] = Cargo.objects.all()
        contexto['tipos_contrato'] = TipoContrato.objects.all()
    elif modelo == 'rol':
        contexto['empleados'] = Empleado.objects.all()
    if request.method == 'POST':
        if id:
            if modelo == 'empleado':
                # Procesamiento específico para Empleado
                objeto.nombre = request.POST.get('nombre')
                objeto.cedula = request.POST.get('cedula')
                objeto.direccion = request.POST.get('direccion')
                objeto.telefono = request.POST.get('telefono')
                objeto.sueldo = float(request.POST.get('sueldo', 0))
                departamento_id = request.POST.get('departamento')
                cargo_id = request.POST.get('cargo')
                tipo_contrato_id = request.POST.get('tipo_contrato')
                
                if departamento_id:
                    objeto.departamento = get_object_or_404(Departamento, pk=departamento_id)
                if cargo_id:
                    objeto.cargo = get_object_or_404(Cargo, pk=cargo_id)
                if tipo_contrato_id:
                    objeto.tipo_contrato = get_object_or_404(TipoContrato, pk=tipo_contrato_id)
                
            elif modelo == 'departamento':
                # Procesamiento para Departamento
                objeto.nombre = request.POST.get('nombre')
                objeto.descripcion = request.POST.get('descripcion')
                
            elif modelo == 'cargo':
                # Procesamiento para Cargo
                objeto.nombre = request.POST.get('nombre')
                objeto.descripcion = request.POST.get('descripcion')
                
            elif modelo == 'tipo_contrato':
                # Procesamiento para TipoContrato
                objeto.nombre = request.POST.get('nombre')
                objeto.descripcion = request.POST.get('descripcion')
                
            elif modelo == 'rol':
                # Procesamiento para Rol de pago
                objeto.periodo = request.POST.get('periodo')
                objeto.fecha_pago = request.POST.get('fecha_pago')
                objeto.horas_extra = int(request.POST.get('horas_extra', 0))
                objeto.descuentos = float(request.POST.get('descuentos', 0))
                objeto.bonificaciones = float(request.POST.get('bonificaciones', 0))
                empleado_id = request.POST.get('empleado')
                
                if empleado_id:
                    objeto.empleado = get_object_or_404(Empleado, pk=empleado_id)
                
                # Calcular total
           
        else:
            # Crear nuevo objeto
            if modelo == 'empleado':
                # Crear nuevo Empleado
                departamento = None
                cargo = None
                tipo_contrato = None
                
                departamento_id = request.POST.get('departamento')
                cargo_id = request.POST.get('cargo')
                tipo_contrato_id = request.POST.get('tipo_contrato')
                
                if departamento_id:
                    departamento = get_object_or_404(Departamento, pk=departamento_id)
                if cargo_id:
                    cargo = get_object_or_404(Cargo, pk=cargo_id)
                if tipo_contrato_id:
                    tipo_contrato = get_object_or_404(TipoContrato, pk=tipo_contrato_id)
                
                objeto = Empleado(
                    nombre=request.POST.get('nombre'),
                    cedula=request.POST.get('cedula'),
                    sexo= request.POST.get('sexo'), 
                    direccion=request.POST.get('direccion'),
                    sueldo=float(request.POST.get('sueldo', 0)),
                    cargo=cargo,
                    departamento=departamento,
                    tipo_contrato=tipo_contrato
                )
                
            elif modelo == 'departamento':
                # Crear nuevo Departamento
                objeto = Departamento(
                    nombre=request.POST.get('nombre'),
                    descripcion=request.POST.get('descripcion')
                )
                
            elif modelo == 'cargo':
                # Crear nuevo Cargo
                objeto = Cargo(
                    nombre=request.POST.get('nombre'),
                    descripcion=request.POST.get('descripcion')
                )
                
            elif modelo == 'tipo_contrato':
                # Crear nuevo TipoContrato
                objeto = TipoContrato(
                    nombre=request.POST.get('nombre'),
                    descripcion=request.POST.get('descripcion')
                )
                
            elif modelo == 'rol':
                # Crear nuevo Rol de Pago
                empleado = None
                empleado_id = request.POST.get('empleado')
                
                if empleado_id:
                    empleado = get_object_or_404(Empleado, pk=empleado_id)
                
                objeto = Rol(
                    periodo=request.POST.get('periodo'),
                    fecha_pago=request.POST.get('fecha_pago'),
                    horas_extra=int(request.POST.get('horas_extra', 0)),
                    descuentos=float(request.POST.get('descuentos', 0)),
                    bonificaciones=float(request.POST.get('bonificaciones', 0)),
                    empleado=empleado
                )
                     
        objeto.save()
        messages.success(request, f"{accion} {modelo} realizado con éxito!")
        return redirect('listar_modelo', modelo=modelo)
    
    return render(request, "modelo/formulario_modelo.html", contexto)

def eliminar_modelo(request, modelo=None, id=None):
    modelos = {
        'empleado': Empleado,
        'departamento': Departamento,
        'cargo': Cargo,
        'tipo_contrato': TipoContrato,
        'rol': Rol,
    }
    if not modelo or modelo not in modelos or not id:
        messages.error(request, "Modelo o ID no válido")
        return redirect('index')
    modelo_seleccionado = modelos[modelo]
    objeto = get_object_or_404(modelo_seleccionado, pk=id)
    
    if request.method == 'POST':
        objeto.delete()
        messages.success(request, f"{modelo.capitalize()} eliminado con éxito!")
        return redirect('listar_modelo', modelo=modelo)

    contexto = {
        'objeto': objeto,
        'modelo': modelo,
    }
    
    return render(request, "eliminacion.html", contexto)