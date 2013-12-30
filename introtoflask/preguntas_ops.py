# -*- coding: utf-8 -*-
from introtoflask import app, lm, principals
from flask import Flask, current_app, render_template, request, flash, redirect, url_for, Blueprint, url_for, session, escape, jsonify
from forms import ContactForm, LoginForm, GroupForm

from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.principal import Principal, Permission, RoleNeed, Identity, identity_changed, AnonymousIdentity, identity_loaded, UserNeed

import json 
from bson import json_util

from introtoflask.models import Usuario
from introtoflask.models import Grupo
from introtoflask.models import Respuesta, Cuestion

from mongoengine import *

from werkzeug.datastructures import MultiDict


preguntas_ops = Blueprint('preguntas', __name__, template_folder='templates/preguntas')

@app.route('/cuestion')
# class ListView(MethodView):
def seeCuestion():
	usuarios = Usuario.objects.all()
	return render_template('usuarios/list.html', usuarios=usuarios)

@app.route('/demo2')
# class ListView(MethodView):
def demo2():
	# usuarios = Usuario.objects.all()

	grupos = [('nombre','eeeee'),('horario','eeeee')]
	usuario = Usuario.objects.get(username='usuario')
	


	Respuesta.mas_id.set_next_value(0)

	respuesta = Respuesta(texto='respuesta de prueba',valor=-33)
	# respuesta._reset_already_indexed('mas_id')
	respuesta2 = Respuesta(texto='respuesta de prueba 2',valor=100)
	respuesta3 = Respuesta(texto='\(\sqrt{3x-1}+(1+x)^2\)',valor=50)
	# cuestion = Cuestion(texto="\left [ - \frac{\hbar^2}{2 m} \frac{\partial^2}{\partial x^2} + V \right ] \Psi = i \hbar \frac{\partial}{\partial t} \Psi",respuesta=[respuesta,respuesta2,respuesta3],conceptos=['demo'])
	cuestion = Cuestion(texto="La cuestión puede contener ecuaciones escritas en LaTeX <code> \( \\frac{3x-1}{(1+x)^3}^2 \) </code>dentro del enunciado.<br/> <code><br/></code>Igualmente se puede introducir ecuaciones eimagenes de esquemas dentro de la pregunta. $$\int_a^b{x}_{0}dx $$",respuesta=[respuesta,respuesta2,respuesta3],conceptos=['demo'])
	cuestion.imagen="static/img/glyphicons-halflings.png"
	return render_template('preguntas/demo.html', usuarios=usuario, grupos=grupos, cuestion=cuestion)



# @app.route('/details/<slug>/')
# @login_required
# def get_details(slug):
# 	usuarios = list(Usuario.objects(nombre=slug))
# 	grupos = list(Grupo.objects.all())
# 	perfil =your_perfil([int(usuarios[0].perfil)])
# 	login = current_user
# 	size = getGroupSize()
# 	return render_template('usuarios/details.html', slug=slug, login =login , usuarios=usuarios, perfiles=perfil, grupos=grupos, size=size)

# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
# 	form = ContactForm()
# 	if request.method == 'POST':
# 		if form.validate() == False:
# 			flash('All fields are required.')
# 			return render_template('contact.html', form=form, action="Add")
# 		else:
# 			usuario =Usuario(nombre=form.nombre.data,apellido=form.apellido.data  ,username=form.username.data, password=form.password.data,perfil=form.perfil.data) # Insert
# 			usuario.save()
# 			return form.nombre.data + " " +form.apellido.data +" ha sido dado de alta"
#  	elif request.method == 'GET':
# 		return render_template('contact.html', form=form, action="Alta")

# @app.route('/contact/<username>', methods=['GET', 'POST'])
# @admin_permission.require(http_exception=403)
# def edit_contact(username):
# 	usuario = Usuario.objects.get(username=username)
# 	user_json=usuario
# 	uuu = [{'nombre':'nombre','username':'username'}]
# 	post = Usuario.objects.get_or_404(username=username)
# 	form = ContactForm(request.form,user_json)
# 	if request.method == 'POST':
# 		if form.validate() == False:
# 			flash('All fields are required.')
# 			return render_template('contact.html', form=form, data_type="Usuarios", action="Editar")
# 		else:
# 			usuario.nombre=form.nombre.data
# 			usuario.username=form.username.data
# 			usuario.password=form.password.data
# 			usuario.perfil=form.perfil.data
# 			# usuario.grupos=[{'nombre':'test1','horario':'LLLLLLL'}]
# 			usuario.save()
# 			# Usuario(nombre=form.nombre.data,apellido=form.lastname.data  ,username=form.username.data, password=form.password.data,perfil=form.perfil.data).save() # Insert
# 			# return form.nombre.data + " " +form.username.data 
# 			return list_users() 
 
# 	elif request.method == 'GET':
# 		print 'GET'
# 		print form.errors	
# 		return render_template('contact.html', form=form, data_type="usuarios", action="Editar")


# @app.route('/grupos/<grupo>', methods=['GET', 'POST'])
# @admin_permission.require(http_exception=403)
# def edit_group(grupo):
# 	# grupo = Grupo.objects.get_or_404(nombre=grupo)
# 	grupo = Grupo.objects.get_or_create(nombre=grupo,defaults={'horario': 'Sin definir'})
# 	grupo_id=grupo[0].id
# 	# if len(grupo[0].horario)<1:
# 	# 	grupo[0].horario = 'Sin definir'
# 	# user_json=usuario
# 	# uuu = [{'nombre':'nombre','username':'username'}]
# 	# post = Usuario.objects.get_or_404(username=username)
# 	form = GroupForm(request.form,grupo[0])
# 	if request.method == 'POST':
# 		if form.validate() == False:
# 			flash('Todos los campos son necesarios.')
# 			return render_template('usuarios/groups.html', form=form, data_type="Grupos", action="Editar")
# 		else:
# 			# flash('Valores por defecto.')
# 			g=Grupo.objects.get(id=grupo_id)
# 			g.update(set__nombre=form.nombre.data)
# 			g.update(set__horario=form.horario.data)
# 			# grupo[0].nombre=form.nombre.data
# 			# grupo[0].horario=form.horario.data
# 			# grupo[0].save()
# 			# return render_template('usuarios/groups.html', form=form, data_type="Grupos", action="Editar")
# 			grupos = Grupo.objects.all()
# 			return render_template ('usuarios/groups.html', grupos=grupos, action="Listar")
# 			# return render_template('grupos.html')
 
# 	elif request.method == 'GET':
# 		return render_template('usuarios/groups.html', form=form, data_type="Grupos", action="Editar")

# @app.route('/grupos', methods=['GET', 'POST'])
# def list_group():
# 	grupos = Grupo.objects.all()
# 	return render_template ('usuarios/groups.html', grupos=grupos, action="Listar")

# @app.route('/grouplist/<group>/')
# # @admin_permission.require(http_exception=403)
# def get_grouplist(group):
# 	# usuarios = Usuario.objects.all()
# 	# usuarios = Usuario.objects(grupos__nombre=group)
# 	g = Grupo.objects.get(nombre=group)
# 	# usuarios = list(Usuario.objects(grupos__nombre=group))
# 	usuarios = list(Usuario.objects(grupo_id=g.id))
# 	grupos = Grupo.objects.all()
# 	# print usuarios.to_json()	
# 	# return slug
# 	# print usuarios
# 	# print group
	
# 	return render_template('usuarios/list_groups.html', group=group, usuarios=usuarios, grupos=grupos)
# 	# return render_template('usuarios/list_groups.html', usuarios=usuarios)

# def getGroupSize():
# 	grupos = Grupo.objects.all()
# 	size = {}
# 	for grupo in grupos:
# 		usuarios = list(Usuario.objects(grupo_id=grupo.id))
# 		count = len(usuarios)
# 		size[grupo.nombre]=count
# 	return size

# def get_context():
# 	usuario = Usuario.objects.get_or_404()
# 	form = self.form(request.form)
# 	context = {
# 		"post": post,
# 		"form": form
# 	}
# 	return context


# def grupos_lst(seleccionado):
# 	grupos_list=[]
# 	options=[]
# 	horarios=[]
# 	iii=1
# 	# for u in Usuario.objects(Q(grupos__exists=True)):
# 	for u in Usuario.objects.all():
#     	# gs.append("[(%d, ",i)
# 		gs = u.grupos[0]
# 		# h = u.grupos[0].horario
# 		if not (gs in grupos_list):
# 			options.append(iii)
# 			# grupos_list.append(g)
# 			horarios.append(u.grupos[0])
# 			iii=iii+1
# 	# print str(zip(options,horarios))
# 	grupos = zip(options,horarios)
# 	return grupos[seleccionado]

# def your_perfil(numero):
# 	perfiles = 'perfil','Alumno','Tutor','Administrador'
# 	n = int(numero[0])
# 	perfil =perfiles[n]
# 	return perfil	

# @app.errorhandler(403)
# def page_not_found(e):
# 	return render_template('admin/403.html'), 403


