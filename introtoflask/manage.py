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


usuarios = Blueprint('usuarios', __name__, template_folder='templates')



normal_role = RoleNeed(u'normal')
normal_permission = Permission(normal_role)
admin_role = RoleNeed(u'Administrador')
admin_permission = Permission(admin_role)



@app.before_request
def log_request():
	if current_app.config.get('LOG_REQUESTS'):
		current_app.logger.debug('whatever')

@lm.user_loader
def load_user(id):
	# print (">>>>>>>>load user = ",Usuario.objects(id=id))
	return Usuario.objects.get(id=id)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
	# login=Usuario.objects.get(username=identity.id['username'])
	login=current_user
	identity.user = login

	if identity.id != None:
		perfil = your_perfil(identity.id[u'perfil'])
		# identity.provides.add(RoleNeed(identity.id[u'perfil']))
		identity.provides.add(RoleNeed(perfil))
	else:
		print "No Admin"
		# print identity.user
		# print current_user
	
	if hasattr(login, 'perfil'):
		print "login no tiene perfil"

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	error = None
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('login.html', form=form)
		else:
			user = form.get_user()
			# session['_id'] = str(user['id'])
			if not user == None and form.password.data == user.password:
				login_user(user)
				print "user perfil"
				print user.perfil
				if user.perfil == '3':
					user_json=json.loads(user.to_json())
					identity = Identity(user_json)
					print 'identity'
					print user_json
					identity_changed.send(current_app._get_current_object(),identity=identity)
					# print(">> Identity: ",identity)

				return render_template('about.html')
			else:
				flash(u"Credenciales incorrectas.")
				return render_template('login.html', form=form)

	elif request.method == 'GET':
		# session.pop('username', None)
		print ("FIN")
		# return render_template('login.html', form=form)
		return render_template('login.html', form=form)

	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	form=LoginForm()
	# session.pop('logged_in', None)
	# session.pop('username', None)
	logout_user()
	# Remove session keys set by Flask-Principal
	for key in ('identity.name', 'identity.auth_type'):
		session.pop(key, None)

	# Tell Flask-Principal the user is anonymous
	identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())

	flash('Se ha desconectado!')
	# return redirect(url_for('home'))
	return render_template('login.html',form=form)

@app.route('/users')
# class ListView(MethodView):
def list_users():
	usuarios = Usuario.objects.all()
	return render_template('usuarios/list.html', usuarios=usuarios)

@app.route('/demo')
# class ListView(MethodView):
def demo():
	# usuarios = Usuario.objects.all()
	grupos = [('nombre','eeeee'),('horario','eeeee')]
	usuario = Usuario.objects.get(username='usuario')
	# usuario.update(add_to_set__grupo_id=["test4"])  # Add an element
	# usuario.update(pull__grupo_id="Test")  # Delete an element
	# usuario.update(pull__grupo_id="Test1")  # Delete an element
	# usuario.update(set__grupo_id=["test3"])  # Just one element
	# usuario.grupo_id("Test3")  # Update
	# usuario.save()
	# usuario.reload()
	# grupo = Grupo.objects.get(nombre='test0')
	# usuario.update(pull__grupos=grupo)
	# usuario.update(add_to_set__grupos=[grupo])
	# usuario.reload()
	# for grupo in usuario.grupo_id:
	# 	grupo = Grupo.objects.get(nombre=grupo)
	# 	grupos.append(grupo)

	respuesta = Respuesta(texto='respuesta de prueba',valor=-33)
	respuesta2 = Respuesta(texto='respuesta de prueba 2',valor=100)
	cuestion = Cuestion(texto='texto del enunciado de prueba',respuesta=[respuesta,respuesta2],conceptos=['demo'])
	
	return render_template('demo.html', usuarios=usuario, grupos=grupos, cuestion=cuestion)



@app.route('/details/<slug>/')
@login_required
def get_details(slug):
	usuarios = list(Usuario.objects(nombre=slug))
	grupos = list(Grupo.objects.all())
	perfil =your_perfil([int(usuarios[0].perfil)])
	login = current_user
	size = getGroupSize()
	return render_template('usuarios/details.html', slug=slug, login =login , usuarios=usuarios, perfiles=perfil, grupos=grupos, size=size)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('contact.html', form=form, action="Add")
		else:
			usuario =Usuario(nombre=form.nombre.data,apellido=form.apellido.data  ,username=form.username.data, password=form.password.data,perfil=form.perfil.data) # Insert
			usuario.save()
			return form.nombre.data + " " +form.apellido.data +" ha sido dado de alta"
 	elif request.method == 'GET':
		return render_template('contact.html', form=form, action="Alta")

@app.route('/contact/<username>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def edit_contact(username):
	usuario = Usuario.objects.get(username=username)
	user_json=usuario
	uuu = [{'nombre':'nombre','username':'username'}]
	post = Usuario.objects.get_or_404(username=username)
	form = ContactForm(request.form,user_json)
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('contact.html', form=form, data_type="Usuarios", action="Editar")
		else:
			usuario.nombre=form.nombre.data
			usuario.username=form.username.data
			usuario.password=form.password.data
			usuario.perfil=form.perfil.data
			# usuario.grupos=[{'nombre':'test1','horario':'LLLLLLL'}]
			usuario.save()
			# Usuario(nombre=form.nombre.data,apellido=form.lastname.data  ,username=form.username.data, password=form.password.data,perfil=form.perfil.data).save() # Insert
			# return form.nombre.data + " " +form.username.data 
			return list_users() 
 
	elif request.method == 'GET':
		print 'GET'
		print form.errors	
		return render_template('contact.html', form=form, data_type="usuarios", action="Editar")


@app.route('/grupos/<grupo>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def edit_group(grupo):
	# grupo = Grupo.objects.get_or_404(nombre=grupo)
	grupo = Grupo.objects.get_or_create(nombre=grupo,defaults={'horario': 'Sin definir'})
	grupo_id=grupo[0].id
	# if len(grupo[0].horario)<1:
	# 	grupo[0].horario = 'Sin definir'
	# user_json=usuario
	# uuu = [{'nombre':'nombre','username':'username'}]
	# post = Usuario.objects.get_or_404(username=username)
	form = GroupForm(request.form,grupo[0])
	if request.method == 'POST':
		if form.validate() == False:
			flash('Todos los campos son necesarios.')
			return render_template('usuarios/groups.html', form=form, data_type="Grupos", action="Editar")
		else:
			# flash('Valores por defecto.')
			g=Grupo.objects.get(id=grupo_id)
			g.update(set__nombre=form.nombre.data)
			g.update(set__horario=form.horario.data)
			# grupo[0].nombre=form.nombre.data
			# grupo[0].horario=form.horario.data
			# grupo[0].save()
			# return render_template('usuarios/groups.html', form=form, data_type="Grupos", action="Editar")
			grupos = Grupo.objects.all()
			return render_template ('usuarios/groups.html', grupos=grupos, action="Listar")
			# return render_template('grupos.html')
 
	elif request.method == 'GET':
		return render_template('usuarios/groups.html', form=form, data_type="Grupos", action="Editar")

@app.route('/grupos', methods=['GET', 'POST'])
def list_group():
	grupos = Grupo.objects.all()
	return render_template ('usuarios/groups.html', grupos=grupos, action="Listar")

@app.route('/grouplist/<group>/')
# @admin_permission.require(http_exception=403)
def get_grouplist(group):
	# usuarios = Usuario.objects.all()
	# usuarios = Usuario.objects(grupos__nombre=group)
	g = Grupo.objects.get(nombre=group)
	# usuarios = list(Usuario.objects(grupos__nombre=group))
	usuarios = list(Usuario.objects(grupo_id=g.id))
	grupos = Grupo.objects.all()
	# print usuarios.to_json()	
	# return slug
	# print usuarios
	# print group
	
	return render_template('usuarios/list_groups.html', group=group, usuarios=usuarios, grupos=grupos)
	# return render_template('usuarios/list_groups.html', usuarios=usuarios)

def getGroupSize():
	grupos = Grupo.objects.all()
	size = {}
	for grupo in grupos:
		usuarios = list(Usuario.objects(grupo_id=grupo.id))
		count = len(usuarios)
		size[grupo.nombre]=count
	return size

def get_context():
	usuario = Usuario.objects.get_or_404()
	form = self.form(request.form)
	context = {
		"post": post,
		"form": form
	}
	return context


def grupos_lst(seleccionado):
	grupos_list=[]
	options=[]
	horarios=[]
	iii=1
	# for u in Usuario.objects(Q(grupos__exists=True)):
	for u in Usuario.objects.all():
    	# gs.append("[(%d, ",i)
		gs = u.grupos[0]
		# h = u.grupos[0].horario
		if not (gs in grupos_list):
			options.append(iii)
			# grupos_list.append(g)
			horarios.append(u.grupos[0])
			iii=iii+1
	# print str(zip(options,horarios))
	grupos = zip(options,horarios)
	return grupos[seleccionado]

def your_perfil(numero):
	perfiles = 'perfil','Alumno','Tutor','Administrador'
	n = int(numero[0])
	perfil =perfiles[n]
	return perfil	

@app.errorhandler(403)
def page_not_found(e):
	return render_template('admin/403.html'), 403


