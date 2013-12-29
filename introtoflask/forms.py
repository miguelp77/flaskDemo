# -*- coding: utf-8 -*-
from flask.ext.wtf import Form

from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, SelectField
from wtforms.validators import Required

from introtoflask.models import Usuario
from introtoflask.models import Grupo
from mongoengine import *


class ContactForm(Form):
	# grupos = Grupo.objects.all()
	
	nombre = TextField("Nombre", [validators.Required("Por favor, introduzca un nombre.")])
	apellido = TextField("Apellido", [validators.Required("Por favor, introduzca un apellido.")])
	username = TextField("Usuario", [validators.Required("Por favor, introduzca un nombre de usuario.")])
	password = TextField(u'Contraseña', [validators.Required(u'Por favor, introduzca una Contraseña.')])
	# perfil = TextField(u'Perfil', [validators.Required("Por favor, introduzca un perfil.")])
	perfil = SelectField(u'Perfil',choices=[('1', 'Alumno'), ('2', 'Tutor'), ('3', 'Administrador')])
	# grupo = SelectField(u'Grupo',choices=[(1, "Abc"), (2, "Def")], default=2)
	# grupos = SelectField(u'Grupo',grupos[0].nombre,coerce=int)
	# grupos = ReferenceField(Grupo,None)

	submit = SubmitField("Enviar")

class LoginForm(Form):
	name = TextField("Nombre", [validators.Required("Please enter your name.")])
	password = PasswordField(u'Contraseña', [validators.Required("Please enter a password.")])
	submit = SubmitField("Enviar")

	def validate_login(self, field):
		usuario = self.get_user()
		if usuario is None:
			raise validators.ValidationError('Usuario invalido')

		if usuario.password != self.password.data:
			raise validators.ValidationError('Contraseña invalida')

	def get_user(self):
		# return Usuario.objects.get(username=self.name.data).first()
		if Usuario.objects(username=self.name.data):
			print ("desde form.py >> ",Usuario.objects.get(username=self.name.data))
			return Usuario.objects.get(username=self.name.data)
		else:
			return None

class GroupForm(Form):
	nombre = TextField("Nombre", [validators.Required("Por favor, introduzca un nombre.")])
	horario = TextField("Horario", [validators.Required("Por favor, introduzca el horario.")])
	submit = SubmitField("Enviar")

class ContactForm_BAK(Form):
	name = TextField("Nombre", [validators.Required("Por favor, introduzca un nombre.")])
	surname = TextField("Apellido", [validators.Required("Por favor, introduzca un apellido.")])
	email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	username = TextField("Usuario", [validators.Required("Por favor, introduzca un nombre de usuario.")])
	password = TextField(u'Contraseña', [validators.Required("Por favor, introduzca un apellido.")])
	subject = TextField("Subject", [validators.Required("Please enter a subject.")])
	message = TextAreaField("Message", [validators.Required("Please enter a message.")])
	submit = SubmitField("Send")

class Cuestion(Form):
	name = TextField("Nombre")
	enunciado = TextField("Enunciado", [validators.Required("Por favor, introduzca un enunciado.")])
	imagen_principal = TextField("Imagen Principal")
	imagen_secundaria = TextField("Imagen Secundaria")
	respuesta = TextField(u'respuesta', [validators.Required("Por favor, introduzca una respuesta.")])
	submit = SubmitField("Enviar")
