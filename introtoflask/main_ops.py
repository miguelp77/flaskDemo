# -*- coding: utf-8 -*-
from introtoflask import app, lm 
from flask import Flask, render_template, request, flash, redirect, url_for, Blueprint, url_for, session, escape, jsonify
from forms import ContactForm, LoginForm

from flask.ext.login import login_user, logout_user, current_user, login_required

from bson import json_util

from introtoflask.models import Usuario
from introtoflask.models import Grupo

from mongoengine import *

main_operations = Blueprint('main_operations', __name__, template_folder='templates')

@app.route('/')
def home():
	"""Page HOME
	Pagina de inicio
	"""
	user = current_user
	return render_template('home.html',user=user)

@app.route('/about')
def about():
	"""Page ABOUT 
	Pagina donde daremos detalles de contacto del adminstrador de la aplicación y del usuario logado
	"""
	return render_template('about.html')

@app.route('/_ajax')
def devuelvo():
	"""Demo AJAX 
	Como actuar con una llamada GET de Ajax"""
	user_id = request.args.get('a')
	user =Usuario.objects.get(id=user_id).to_json()
	b=json_util.dumps(user)
	return user

@app.route('/_addGroup')
def addGroup():
	""" Pendiente de terminar
	Incluir como añadir un grupo a una asignatura"""
	user_id = request.args.get('a')
	usuario =Usuario.objects.get(id=user_id).to_json()

@app.route('/_addGroupToUser')
def addGroupToUser():
	"""Añadir un grupo a un usuario
	Atiende a la llamada AJAX con la que se añade un grupo a un usuario
	"""
	user = request.args.get('u')
	groups = request.args.get('g')
	if len(groups) > 1:
		groups = groups.split(',')
	print groups
	usuario =Usuario.objects.get(id=user)
	for group_id in groups:
		grupo = Grupo.objects.get(id=group_id)
		# usuario.update(add_to_set__grupos=grupo)
		usuario.update(add_to_set__grupo_id=[grupo.id])
	return "200"

@app.route('/_removeGroup')
def removeGroup():
	"""Eliminar un grupo a un usuario
	Atiende a la llamada AJAX con la que se elimina un grupo a un usuario
	"""
	user_id = request.args.get('u')
	grupo_id = request.args.get('g')
	usuario = Usuario.objects.get(id=user_id).update(pull__grupos__id=grupo_id)
	return "200"

def uniqueName(user_id,name):
	"""REVISAR  Unico nombre
	unico nombre. Posiblemente se pueda eliminar
	"""	
	grupo = Usuario.objects(id=user_id, grupos__nombre__iexact=nombre)
	# grupo = Grupo.objects.get(nombre__iexact=name)
	if len(grupo) > 0:
		return False
	return True
