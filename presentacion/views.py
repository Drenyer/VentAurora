from django.shortcuts import render
from django.http import HttpResponse
from firebase_config import FirebaseDB
from firebase_admin import db

# Rutas y URL de Firebase
path = "d:/Instituto-4Ciclo/PROYECTO INTEGRADOR/Aplicaciones Empresariales/Prototipo2-pagina/administrador/Interfaz/project_credentials.json"
url = "https://respaldor-84fa0-default-rtdb.firebaseio.com/"
fb_db = FirebaseDB(path, url)

# Vista para la página de inicio
def Inicio(request):
    return render(request, 'Inicio.html')

# Vista para la página "Sobre Nosotros"
def SobreN(request):
    return render(request, 'SobreN.html')

# Vista para la página de contacto
def Contacto(request):
    return render(request, 'Contacto.html')

# Vista para la página de inicio de sesión
def IniciarSession(request):
    return render(request, 'Isession.html') 

# Vista para la página de consultas
def Consultas(request):
    return render(request, 'ConsultasA.html')

# Vista para la página de registro de usuarios
def RegistroU(request):
    return render(request, 'RegistrarU.html')

# Función para autenticar usuarios
def Autenticar(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        contraseña = request.POST.get('contraseña')

        data = fb_db.read_record("usuarios")

        # Iterar sobre los usuarios y verificar las credenciales
        for users, usuarios in data.items():
            if usuarios['usuarioRef'] == usuario and usuarios['contraseña'] == contraseña:
                # Iniciar sesión y redirigir al usuario a la página de inicio si las credenciales son válidas
                return Inicio(request)
        
        # Devolver un mensaje de error si las credenciales son incorrectas
        return HttpResponse("Error al iniciar sesión. Credenciales incorrectas.")

# Función para registrar usuarios en la base de datos
def RegistrarUBD(request):
    if request.method == 'POST':
        correo = request.POST.get('correo1')
        usuario = request.POST.get('usuario1')
        contraseña1 = request.POST.get('contraseña1')
        contraseña2 = request.POST.get('contraseña2')

        # Verificar que las contraseñas coincidan
        if contraseña1 != contraseña2:
            return HttpResponse("Las contraseñas no son iguales.")
        
        usuarios_ref = db.reference('/users')
        datos_usuarios = usuarios_ref.get()

        # Verificar si el usuario ya existe en la base de datos
        if datos_usuarios:
            for info_usuario in datos_usuarios.values():
                if info_usuario.get('usuario') == usuario:
                    return HttpResponse("El usuario ya existe. Intente con otro nombre de usuario.")
         
        data = {
            'email': correo,
            'usuarioRef': usuario,
            'contraseña': contraseña1   
        }

        try:
            # Guardar el registro del usuario en la base de datos Firebase
            fb_db.write_record(f'/usuarios/{usuario}', data)
            return render(request,'Isession.html')
        except Exception as e:
            return HttpResponse(f"Error al guardar en la base de datos: {str(e)}")

    return render(request, 'Inicio.html')

# Función para ver los datos de usuarios almacenados en la base de datos
def VerdatosUBD(request):
    data = fb_db.read_record("usuarios")
    
    # Convertir el diccionario de datos en una lista de tuplas para la plantilla
    results = [(key, value['email'], value['contraseña']) for key, value in data.items()]
    
    return render(request, 'Verdatos.html', {'results': results})

# Función para eliminar usuarios de la base de datos
def EliminarUBD(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        
        # Eliminar el registro del usuario de la base de datos
        fb_db.delete_record(f'/usuarios/{usuario_id}')

        return VerdatosUBD(request)

# Función para preparar la actualización de datos de usuario
def Iractualizar(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        data = fb_db.read_record(f'/usuarios/{usuario_id}')
        
        # Obtener los datos del usuario si existen
        if isinstance(data, dict):
            email = data.get('email', '')
            contrasena = data.get('contraseña', '')
        else:
            email, contrasena = '', '', ''
        
        context = {
            'usuario_id': usuario_id,
            'email': email,
            'contrasena': contrasena,
        }
        
        return render(request, 'Actualizar.html', context)

# Función para actualizar los datos de usuario en la base de datos
def ActulizarUBD(request):
    if request.method == 'POST':
        correo = request.POST.get('correo1')
        usuario = request.POST.get('usuario_id')
        contraseña1 = request.POST.get('contraseña1')
        contraseña2 = request.POST.get('contraseña2')

        # Verificar que las contraseñas coincidan
        if contraseña1 != contraseña2:
            return HttpResponse("Las contraseñas no son iguales.")
         
        data = {
            'email': correo,
            'contraseña': contraseña1   
        }

        try:
            # Actualizar los datos del usuario en la base de datos Firebase
            fb_db.update_record(f'/usuarios/{usuario}', data)
            return VerdatosUBD(request)
        except Exception as e:
            return HttpResponse(f"Error al guardar en la base de datos: {str(e)}")
        
# Función para consultar el tiempo total de un usuario
def ConsultaTime(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')

        # Obtener los datos del usuario desde Firebase
        data = fb_db.read_record(f"/Time/{usuario}")

        # Inicializar la suma total del tiempo
        tiempo_total = 0

        # Iterar sobre los registros y sumar los valores de "tiempo"
        for fecha, registro in data.items():
            tiempo_total += registro.get('tiempo', 0)

        data = {
            'tiempototal': tiempo_total
        }

        # Devolver el resultado como una respuesta HTTP
        return render(request, 'Consulta1.html', data)

# Función para consultar la cantidad de productos de un usuario
def ConsultaCant(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')

        # Obtener los datos de productos desde Firebase
        data = fb_db.read_record("/productos")

        # Inicializar la cantidad total de productos
        cantidad_total = 0

        # Iterar sobre los registros de productos y contar los que pertenecen al usuario
        for producto_id, producto_data in data.items():
            if producto_data.get('id_usuario') == usuario:
                cantidad_total += 1
        
        # Preparar los datos para la plantilla
        context = {
            'cantidad_total': cantidad_total,
            'usuario': usuario
        }

        # Devolver el resultado como una respuesta HTTP
        return render(request, 'Consulta2.html', context)

# Función para consultar el tiempo total de cada usuario y mostrar los 3 principales
def ConsultaHora(request):
    if request.method == 'POST':
        # Obtener los datos de tiempo desde Firebase
        data = fb_db.read_record("/Time")

        # Diccionario para almacenar el tiempo total de cada usuario
        usuarios_tiempos = {}

        # Iterar sobre los registros de usuarios
        for usuario, fechas in data.items():
            # Inicializar el tiempo total para el usuario
            tiempo_total = 0
            # Sumar los tiempos para cada fecha
            for fecha, registro in fechas.items():
                tiempo_total += registro.get('tiempo', 0)
            # Almacenar el tiempo total en el diccionario
            usuarios_tiempos[usuario] = tiempo_total

        # Ordenar los usuarios por tiempo total de mayor a menor
        usuarios_ordenados = sorted(usuarios_tiempos.items(), key=lambda x: x[1], reverse=True)

        # Seleccionar los tres primeros usuarios
        top_3_usuarios = usuarios_ordenados[:3]

        # Preparar los datos para la plantilla
        context = {
            'top_3_usuarios': top_3_usuarios
        }

        # Renderizar la respuesta
        return render(request, 'Consulta3.html', context)

# Función para buscar usuarios por los primeros 3 caracteres de su usuarioRef
def ConsultaBuscar(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario').lower()  # Convertir a minúsculas

        # Obtener los datos de usuarios desde Firebase
        data = fb_db.read_record("/usuarios")

        encontrados = {}

        # Función para comparar los primeros 3 caracteres
        def compara_hasta_tres_caracteres(cadena1, cadena2):
            # Limitar la comparación a los primeros 3 caracteres
            for c1, c2 in zip(cadena1[:3], cadena2[:3]):
                if c1.lower() != c2.lower():
                    return False
            return True

        # Iterar sobre los usuarios y comparar los primeros 3 caracteres de usuarioRef (en minúsculas)
        for user_id, user_data in data.items():
            if 'usuarioRef' in user_data and compara_hasta_tres_caracteres(usuario, user_data['usuarioRef']):
                encontrados[user_id] = user_data

        context = {
            'encontrados': encontrados
        }

        return render(request, 'Consulta4.html', context)

# Función para consultar usuarios que tengan productos registrados
def ConsultaUPRegistrados(request):
    if request.method == 'POST':
        # Obtener los datos de productos y usuarios desde Firebase
        productos_data = fb_db.read_record("/productos")
        usuarios_data = fb_db.read_record("/usuarios")

        usuarios_con_productos = set()

        # Iterar sobre los productos y agregar usuarios con productos a un set
        for producto_id, producto_data in productos_data.items():
            if 'id_usuario' in producto_data:
                usuarios_con_productos.add(producto_data['id_usuario'])

        # Filtrar los usuarios que tienen productos registrados
        encontrados = {user_id: usuarios_data[user_id] for user_id in usuarios_con_productos}

        context = {
            'encontrados': encontrados
        }

        return render(request, 'Consulta5.html', context)
