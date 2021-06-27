from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import bcrypt
from .models import *
from datetime import datetime


def inicio(request):
    return render(request,"inicio.html")

def registro(request):
    if request.method=="POST":
        usuario = Usuario(
            nombre = request.POST["nombre"],
            email = request.POST["email"],
            password = request.POST["password"]
        )
        if Usuario.objects.filter(email = request.POST["email"]).exists():
            messages.warning(request,"Este email ya esta registrado")
            return redirect("/")
        errors = Usuario.objects.validacionesBasicas(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.warning(request,f" {value} en el campo {key}")
            return redirect("/")

        else:
            password = bcrypt.hashpw(usuario.password.encode(), bcrypt.gensalt())
            usuario.password = password.decode()
            usuario.save()
            messages.success(request,"Usuario creado con exito")
            return redirect("/")

def login(request):
    if request.method=="POST":
        usuario = Usuario.objects.filter(email = request.POST["email"])

        if len(usuario) == 0:
            messages.warning(request,"Email o contraseña incorrectos")
            return redirect("/")

        usuario = usuario[0]

        if not bcrypt.checkpw(request.POST['password'].encode(), usuario.password.encode()):
            messages.warning(request, "Email o contraseña incorrectos.")
            return redirect("/")

        request.session["nombre"] = usuario.nombre
        request.session["id_usuario"] = usuario.id

        return redirect("/bienvenido")

def logout(request):
    try:
        del request.session["nombre"]
        messages.success(request,"Vuelve pronto")
    except:
        return redirect("/")
    return redirect("/")

def bienvenido(request):
    if request.method=="GET" and "nombre" in request.session:
        usuario_actual = request.session["nombre"]
        context ={
            "usuario_actual": usuario_actual
        }
        return render(request,"bienvenido.html",context)
    else:
        messages.warning(request,"Debes iniciar sesion para ver esta pagina")
        return redirect("/")

def citas(request, idUsuario):
    if request.method =="GET" and "nombre" in request.session and request.session["id_usuario"] == idUsuario:
        usuario_actual = request.session["nombre"]
        usuario_id = request.session["id_usuario"]
        citas = Cita.objects.all()
        hoy = datetime.now().date()

        try:
            usuario = Usuario.objects.get(id = idUsuario)
        except ObjectDoesNotExist:
            messages.warning(request,"El usuario no existe")
        context = {
            "hoy": hoy,
            "citas": citas,
            "usuario_actual": usuario_actual,
            "usuario": usuario,
            "usuario_id": usuario_id
        }
        return render(request, "perfil.html",context)
    if request.method =="GET" and "nombre" not in request.session:
        messages.warning(request,"No puedes realizar esta accion")
        return redirect("/")
    if request.method =="GET" and request.session["id_usuario"] != idUsuario:
        usuario_id = request.session["id_usuario"]
        messages.warning(request,"no puedes realizar esto")
        return redirect(f"/citas/{usuario_id}")

def agregar(request, idUsuario):

    get_citas = Usuario.objects.get(id = idUsuario)
    if request.method=="GET" and "nombre" in request.session:
        usuario_actual = request.session["nombre"]
        get_citas = Usuario.objects.get(id = idUsuario)
        context = {
            "usuario_actual": usuario_actual,
            "perfil": get_citas
        }
        return render(request,"agregar.html",context)
    
    elif request.method =="POST":
        usuario = Usuario.objects.get(nombre = request.session["nombre"])
        cita = Cita(
            tarea = request.POST["tarea"],
            fecha = request.POST["fecha"],
            estado = request.POST["estado"],
            usuario = usuario
        )
        errors = Cita.objects.validacionesBasicas(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.warning(request,f" {value} en el campo {key}")
                return redirect(f"/citas/agregar/{get_citas.id}")
        cita.save()
        return redirect(f"/citas/{get_citas.id}")
        

    else:
        messages.warning(request,"No puedes realizar esta accion")
        return redirect("/")

def editar(request,idCita):
    get_cita = Cita.objects.get(id = idCita)
    if request.method == "GET" and "nombre" in request.session and request.session["id_usuario"] == get_cita.usuario.id:
        usuario_actual = request.session["nombre"]
        context = {
            "usuario_actual": usuario_actual,
            "get_cita": get_cita
        }
        return render(request,"editar.html",context)
    elif request.method =="POST":
        cita = Cita.objects.get(id = idCita)
        tarea = request.POST.get("tarea")
        fecha = request.POST.get("fecha")
        estado = request.POST.get("estado")
        errors = Cita.objects.validacionesBasicas(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.warning(request,f" {value} en el campo {key}")
                return redirect(f"/citas/editar/{get_cita.id}")
        cita.tarea = tarea
        cita.fecha = fecha
        cita.estado = estado
        cita.save()
        return redirect(f"/citas/{get_cita.usuario.id}")
    if request.method == "GET" and request.session["id_usuario"] != get_cita.usuario.id:
        messages.warning(request,"No puedes realizar esta accion")
        return redirect(f"/citas/{get_cita.usuario.id}")

    if request.method == "GET" and "nombre" not in request.session:
        messages.warning(request,"Debes iniciar sesion para usar esto")
        return redirect("/")



def eliminar(request, idCita):
    get_cita = Cita.objects.get(id = idCita)
    if request.method == "GET" and "nombre" in request.session and request.session["id_usuario"] == get_cita.usuario.id:
        usuario_actual = request.session["nombre"]
        context = {
            "usuario_actual": usuario_actual,
        }
        return render(request,"eliminar.html",context)
    elif request.method =="POST":
        get_cita = Cita.objects.get(id = idCita)
        get_cita.delete()
        return redirect(f"/citas/{get_cita.usuario.id}")
    if request.method == "GET" and request.session["id_usuario"] != get_cita.usuario.id:
        messages.warning(request,"No puedes realizar esta accion")
        return redirect(f"/citas/{get_cita.usuario.id}")

    if request.method == "GET" and "nombre" not in request.session:
        messages.warning(request,"No puedes realizar esta accion")
        return redirect("/")