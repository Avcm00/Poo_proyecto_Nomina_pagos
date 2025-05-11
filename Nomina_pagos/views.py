from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .models import Empleado, Departamento, Cargo, TipoContrato, Rol

def login(request):
    return render(request, "login/login.html")
  
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
    """
    Vista dinámica que muestra un listado de cualquier modelo según el parámetro.
    
    Parámetros:
    - modelo: String con el nombre del modelo a mostrar (empleado, departamento, cargo, tipo_contrato, rol)
    """
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
    """
    Vista para mostrar el detalle de un registro específico.
    
    Parámetros:
    - modelo: String con el nombre del modelo a mostrar
    - id: ID del registro a mostrar
    """
    # Diccionario que mapea nombres de modelos a las clases correspondientes
    modelos = {
        'empleado': Empleado,
        'departamento': Departamento,
        'cargo': Cargo,
        'tipo_contrato': TipoContrato,
        'rol': Rol,
    }
    
    # Si no se especifica un modelo o el modelo no existe, redirigir al inicio
    if not modelo or modelo not in modelos or not id:
        messages.error(request, "Modelo o ID no válido")
        return redirect('index')
    
    # Obtener el modelo seleccionado
    modelo_seleccionado = modelos[modelo]
    
    # Obtener el objeto específico o retornar 404 si no existe
    objeto = get_object_or_404(modelo_seleccionado, pk=id)
    
    # Contexto para la plantilla
    contexto = {
        'objeto': objeto,
        'modelo': modelo,
    }
    
    return render(request, "modelo/detalle_modelo.html", contexto)

def formulario_modelo(request, modelo=None, id=None):
    """
    Vista para crear o editar un registro.
    
    Parámetros:
    - modelo: String con el nombre del modelo a editar/crear
    - id: ID del registro a editar (None para crear nuevo)
    """
    # Diccionario que mapea nombres de modelos a las clases correspondientes
    modelos = {
        'empleado': Empleado,
        'departamento': Departamento,
        'cargo': Cargo,
        'tipo_contrato': TipoContrato,
        'rol': Rol,
    }
    
    # Si no se especifica un modelo o el modelo no existe, redirigir al inicio
    if not modelo or modelo not in modelos:
        messages.error(request, "Modelo no válido")
        return redirect('index')
    
    # Obtener el modelo seleccionado
    modelo_seleccionado = modelos[modelo]
    
    # Inicializar variables
    objeto = None
    accion = "Crear"
    
    # Si se proporciona ID, es una edición
    if id:
        objeto = get_object_or_404(modelo_seleccionado, pk=id)
        accion = "Editar"
    
    # Inicializar contexto
    contexto = {
        'objeto': objeto,
        'modelo': modelo,
        'accion': accion,
    }
    
    # Agregar datos adicionales al contexto según el modelo
    if modelo == 'empleado':
        contexto['departamentos'] = Departamento.objects.all()
        contexto['cargos'] = Cargo.objects.all()
        contexto['tipos_contrato'] = TipoContrato.objects.all()
    elif modelo == 'rol':
        contexto['empleados'] = Empleado.objects.all()
    
    # Procesar el formulario si es POST
    if request.method == 'POST':
        # Crear un nuevo objeto o actualizar uno existente
        if id:
            # Actualizar objeto existente
            if modelo == 'empleado':
                # Procesamiento específico para Empleado
                objeto.nombre = request.POST.get('nombre')
                objeto.apellido = request.POST.get('apellido')
                objeto.cedula = request.POST.get('cedula')
                objeto.direccion = request.POST.get('direccion')
                objeto.telefono = request.POST.get('telefono')
                objeto.email = request.POST.get('email')
                objeto.fecha_nacimiento = request.POST.get('fecha_nacimiento')
                objeto.fecha_contratacion = request.POST.get('fecha_contratacion')
                objeto.salario_base = float(request.POST.get('salario_base', 0))
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
                    apellido=request.POST.get('apellido'),
                    cedula=request.POST.get('cedula'),
                    direccion=request.POST.get('direccion'),
                    telefono=request.POST.get('telefono'),
                    email=request.POST.get('email'),
                    fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                    fecha_contratacion=request.POST.get('fecha_contratacion'),
                    salario_base=float(request.POST.get('salario_base', 0)),
                    departamento=departamento,
                    cargo=cargo,
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
                
                # Calcular total para el nuevo rol
                
        
        # Guardar el objeto
        objeto.save()
        
        # Mensaje de éxito
        messages.success(request, f"{accion} {modelo} realizado con éxito!")
        
        # Redirigir al listado
        return redirect('listar_modelo', modelo=modelo)
    
    return render(request, "modelo/formulario_modelo.html", contexto)

def eliminar_modelo(request, modelo=None, id=None):
    """
    Vista para eliminar un registro.
    
    Parámetros:
    - modelo: String con el nombre del modelo a eliminar
    - id: ID del registro a eliminar
    """
    # Diccionario que mapea nombres de modelos a las clases correspondientes
    modelos = {
        'empleado': Empleado,
        'departamento': Departamento,
        'cargo': Cargo,
        'tipo_contrato': TipoContrato,
        'rol': Rol,
    }
    
    # Si no se especifica un modelo o el modelo no existe, redirigir al inicio
    if not modelo or modelo not in modelos or not id:
        messages.error(request, "Modelo o ID no válido")
        return redirect('index')
    
    # Obtener el modelo seleccionado
    modelo_seleccionado = modelos[modelo]
    
    # Obtener el objeto específico o retornar 404 si no existe
    objeto = get_object_or_404(modelo_seleccionado, pk=id)
    
    if request.method == 'POST':
        # Eliminar el objeto
        objeto.delete()
        
        # Mensaje de éxito
        messages.success(request, f"{modelo.capitalize()} eliminado con éxito!")
        
        # Redirigir al listado
        return redirect('listar_modelo', modelo=modelo)
    
    # Si es GET, mostrar confirmación de eliminación
    contexto = {
        'objeto': objeto,
        'modelo': modelo,
    }
    
    return render(request, "confirmar_eliminacion.html", contexto)