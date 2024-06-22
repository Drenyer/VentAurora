from django.urls import path
from . import views

# Nombre de la aplicación
app_name = 'Presentacion'

# Definición de las URLs
urlpatterns = [
    path('', views.Inicio, name='inicio'),  
    # Ruta para la página de inicio
    path('sobrenosotros', views.SobreN, name='sobre'),  
    # Ruta para la página "Sobre Nosotros"
    path('contacto', views.Contacto, name='contacto'),  
    # Ruta para la página de contacto
    path('autenticar', views.Autenticar, name='autenticar'),  
    # Ruta para la autenticación de usuarios
    path('verdatos', views.VerdatosUBD, name='datos'),  
    # Ruta para ver los datos de usuarios registrados
    path('consultasavanzadas', views.Consultas, name='consultas'),  
    # Ruta para la página de consultas avanzadas
    path('iniciarsession', views.IniciarSession, name='Isession'),  
    # Ruta para iniciar sesión
    path('registro', views.RegistroU, name='Rusuario'),  
    # Ruta para la página de registro de usuarios
    path('val2', views.RegistrarUBD, name='registrarUBD'),  
    # Ruta para registrar un nuevo usuario en la base de datos
    path('val3', views.EliminarUBD, name='eliminarUBD'),  
    # Ruta para eliminar un usuario de la base de datos
    path('val4', views.Iractualizar, name='iractualizar'),  
    # Ruta para ir a la página de actualización de datos de usuario
    path('val5', views.ActulizarUBD, name='actualizarUBD'),  
    # Ruta para actualizar datos de usuario en la base de datos
    path('consulta1', views.ConsultaTime, name='consultaTiempo'),  
    # Ruta para la consulta de tiempo de un usuario
    path('consulta2', views.ConsultaCant, name='consultaCantidad'),  
    # Ruta para la consulta de cantidad de productos por usuario
    path('consulta3', views.ConsultaHora, name='consultaHoras'),  
    # Ruta para la consulta de horas trabajadas por usuario
    path('consulta4', views.ConsultaBuscar, name='consultaBuscar'),  
    # Ruta para la consulta específica de búsqueda de usuarios
    path('consulta5', views.ConsultaUPRegistrados, name='ConsultaUPR'),  
    # Ruta para la consulta de usuarios con productos registrados
]
