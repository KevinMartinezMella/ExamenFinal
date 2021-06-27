from django.urls import path
from . import views

urlpatterns =[
    path("",views.inicio, name="inicio"),
    path("login",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("registro",views.registro,name="registro"),
    path("bienvenido",views.bienvenido, name="bienvenido"),
    path("citas/<int:idUsuario>",views.citas, name="citas"),
    path("citas/agregar/<int:idUsuario>",views.agregar, name="agregar"),
    path("citas/editar/<int:idCita>",views.editar, name="editar"),
    path("citas/eliminar/<int:idCita>",views.eliminar,name="eliminar")
]