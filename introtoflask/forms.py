# -*- coding: utf-8 -*-
from flask.ext.wtf import Form

from werkzeug import FileStorage

from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, SelectField, FieldList, FormField
from wtforms.fields import FileField
# from flask_wtf.file import FileField
from wtforms.validators import Required

# from introtoflask.models import Usuario
# from introtoflask.models import Grupo

# from mongoengine import *


class ContactForm(Form):
	nombre = TextField("Nombre", [validators.Required("Por favor, introduzca un nombre.")])
	apellido = TextField("Apellido", [validators.Required("Por favor, introduzca un apellido.")])
	username = TextField("Usuario", [validators.Required("Por favor, introduzca un nombre de usuario.")])
	password = TextField(u'Contraseña', [validators.Required(u'Por favor, introduzca una Contraseña.')])
	perfil = SelectField(u'Perfil',choices=[('1', 'Alumno'), ('2', 'Tutor'), ('3', 'Administrador')])
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

class AnswerForm(Form):
	texto = TextField("Respuesta")
	valor = TextField("Valor")

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(AnswerForm, self).__init__(*args, **kwargs)

class testForm(Form):
	description  = TextAreaField(u'Image Description')
	fileName = FileField(u'Image File','attachment')
	Enviar = SubmitField('Enviar')

class QuestForm(Form):
	descripcion = TextField(u"Descripción")
	enunciado = TextAreaField("Enunciado", [validators.Required("Por favor, introduzca un enunciado.")])
	imagen_principal = TextField("Imagen Principal")
	imagen_secundaria = TextField("Imagen Secundaria")
	respuestas = FieldList(FormField(AnswerForm), min_entries = 2)
	imagen = FileField(u'Imagen Principal','attachment')
	imagen_aux = FileField(u'Imagen Secundaria','attachment')
	submit = SubmitField("Enviar")

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(QuestForm, self).__init__(*args, **kwargs)

