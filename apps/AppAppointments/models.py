from django.db import models
import re
from datetime import datetime, timedelta, date


from django.db.models.deletion import CASCADE


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')


class UsuarioManager(models.Manager):
    def validacionesBasicas(self, usuario):

        errors = {}

        validarLongitud("nombre", usuario["nombre"], errors, 2, 20,)
        validarLongitud("email", usuario["email"], errors, 10, 50,)
        validarLongitud("password", usuario["password"], errors, 8, 40,)

        if not EMAIL_REGEX.match(usuario["email"]):
            errors["email"] = "El email no tiene un formato valido"

        if usuario["password"] != usuario["confirmPassword"]:
            errors["password"] = "Las contraseñas no coinciden"

        return errors

class Usuario(models.Model):
    nombre = models.CharField(max_length=20)
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre}"

class CitaManager(models.Manager):
    def validacionesBasicas(self, cita):
        errors = {}
        today = datetime.now()

        
        validarLongitud("tarea", cita["tarea"], errors, 2, 50,)
        validarLongitud("fecha", cita["fecha"], errors, 10, 50,)

        if cita['fecha'] == '':
            errors["fecha"] = "Porfavor selecciona una fecha"

        elif cita["fecha"] <= str(today):
            errors["fecha"] = "Tu cita no debe ser una fecha pasada"
        

        return errors


class Cita(models.Model):
    usuario = models.ForeignKey(Usuario, related_name="citas", on_delete=models.CASCADE)
    tarea = models.CharField(max_length=120)
    fecha = models.DateField()
    estado = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CitaManager()

    class Meta:
        ordering = ["fecha"]



def validarLongitud(campo, cadena, errors, minimo, maximo):
    if len(cadena) < minimo or len(cadena) > maximo:
        errors[campo] =f"El {campo} no debe ser menor a {minimo} y {maximo} caracteres"
