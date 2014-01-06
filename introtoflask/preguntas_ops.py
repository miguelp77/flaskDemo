# -*- coding: utf-8 -*-
from introtoflask import app, lm, principals
from flask import Flask, current_app, render_template, request, flash, redirect, url_for, Blueprint, session, escape, jsonify, send_from_directory
from forms import QuestForm, AnswerForm, testForm

from flask.ext.wtf import Form

from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.principal import Principal, Permission, RoleNeed, Identity, identity_changed, AnonymousIdentity, identity_loaded, UserNeed
from bson import json_util
import json 
import os


from flask.ext.thumbnails import Thumbnail

from introtoflask.models import Usuario
from introtoflask.models import Grupo
from introtoflask.models import Respuesta, Cuestion

from mongoengine import *

from werkzeug.datastructures import MultiDict
from werkzeug import secure_filename

preguntas_ops = Blueprint('preguntas', __name__, template_folder='preguntas/templates/preguntas/')

admin_role = RoleNeed(u'Administrador')
admin_permission = Permission(admin_role)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/media/<filename>')
def media_file(filename):
	return send_from_directory(app.config['MEDIA_THUMBNAIL_FOLDER'], filename)


def checkfile(form,field):
	if field.data:
		filename=field.data.lower()
		ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
		if not ('.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS):
			raise ValidationError('Wrong Filetype, you can upload only png,jpg,jpeg,gif files')
		else:
			raise ValidationError('field not Present') # I added this justfor some debugging

def allowed_file(field):
	if field.filename:
		filename=field.filename.lower()
		print "filename " + filename
		print str('.' in filename)
		print str(filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS)
		print "AMBAS TRUE?"
		if not ('.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
			raise ValidationError('Wrong Filetype, you can upload only png,jpg,jpeg,gif files')
		return True
	else:
		raise ValidationError(filename + ' field not Present in ' + str(ALLOWED_EXTENSIONS))

# @app.route('/cuestion')
# # class ListView(MethodView):
# def seeCuestion():
# 	usuarios = Usuario.objects.all()
# 	return render_template('usuarios/list.html', usuarios=usuarios)



@app.route('/cuestion', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def edit_question():
	cuestion = Cuestion.objects.all()
	usuario= current_user
	grupos = [('nombre','eeeee'),('horario','eeeee')]

	form_respuesta = "AnswerForm(request.form, Respuesta)"
	# form = QuestForm(request.form, cuestion)
	form = QuestForm()
	form2 = testForm()
	if request.method == 'POST':
		file = request.files['imagen']
		file_aux= request.files['imagen_aux']
		# file = request.form.get('imagen')
		app.logger.debug(file.filename)
		# file = request.files['imagen']
		# print bool(allowed_file(file))
		if file and allowed_file(file):
			filename = secure_filename(file.filename)
			print "FILENAME: " + filename
			print app.config['MEDIA_FOLDER']
			print file.save(os.path.join(app.config['MEDIA_FOLDER'], filename))
			print "FILENAME2: " + filename
			if form.submit.data:
				r_len = len(form.respuestas.data) - 1
				if len(form.respuestas[r_len].texto.data) > 1:
					form.respuestas.append_entry(u'default')
					return render_template('form_pregunta.html', form=form, action="EditarPOST")
				else:
					cuestion = Cuestion(texto=form.enunciado.data, conceptos=['demo','test'])
					cuestion.imagen = app.config['MEDIA_URL'] + file.filename
					if file_aux and allowed_file(file_aux):
						cuestion.imagen_aux = app.config['MEDIA_URL'] + file_aux.filename
					cuestion.creada_por=get_username(current_user)
					for r in form.respuestas.data:
						if r['texto']:
							respuesta_n = Respuesta(texto=r['texto'],valor=int(r['valor']))
							cuestion.respuesta.append(respuesta_n)
					cuestion.save()
					return render_template('resumen.html', usuarios=usuario, grupos=grupos, cuestion=cuestion, login=current_user)

		if form.validate == False:
			print form.errors
			flash('All fields are required.')
			return render_template('form_pregunta.html', form=form, action="EditarPOST")
		else:
			print form.errors
			if form.submit.data:
				r_len = len(form.respuestas.data) - 1
				if len(form.respuestas[r_len].texto.data) > 1:
					form.respuestas.append_entry(u'default')
					return render_template('form_pregunta.html', form=form, action="EditarPOST")
				else:
					cuestion = Cuestion(texto=form.enunciado.data, conceptos=['demo','test'])
					# cuestion.imagen = app.config['MEDIA_URL'] + file.filename
					cuestion.creada_por=get_username(current_user)
					for r in form.respuestas.data:
						respuesta_n = Respuesta(texto=r['texto'],valor=r['valor'])
						cuestion.respuesta.append(respuesta_n)
						
					# file = request.files['imagen']
			# respuesta1 = Respuesta(texto=form.respuestas[0].texto.data, valor=form.respuestas[0].valor.data )
			# respuesta2 = Respuesta(texto=form.respuestas[1].texto.data, valor=form.respuestas[1].valor.data )
					return render_template('resumen.html', usuarios=usuario, grupos=grupos, cuestion=cuestion, login=current_user)

	elif request.method == 'GET':
		return render_template('form_pregunta.html', form=form, action="Editar")


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

def get_username(id):
	usuario = Usuario.objects.get(id=id)
	return usuario.username

@app.route('/demo2')
# class ListView(MethodView):
def demo2():
	# usuarios = Usuario.objects.all()

	grupos = [('nombre','eeeee'),('horario','eeeee')]
	usuario = Usuario.objects.get(username='usuario')
	
	Respuesta.mas_id.set_next_value(0)

	respuesta = Respuesta(texto='respuesta de prueba',valor=-33)
	respuesta4 = Respuesta(texto='respuesta de prueba 4',valor=-33)
	# respuesta._reset_already_indexed('mas_id')
	respuesta2 = Respuesta(texto='respuesta de prueba 2',valor=100)
	respuesta3 = Respuesta(texto='\(\sqrt{3x-1}+(1+x)^2\)',valor=50)
	# cuestion = Cuestion(texto="\left [ - \frac{\hbar^2}{2 m} \frac{\partial^2}{\partial x^2} + V \right ] \Psi = i \hbar \frac{\partial}{\partial t} \Psi",respuesta=[respuesta,respuesta2,respuesta3],conceptos=['demo'])
	cuestion = Cuestion(texto=u"Enunciado con ecuaciones e imagenes de esquemas dentro de la pregunta. $$\int_a^b{x}_{0}dx $$ La cuestión puede contener ecuaciones escritas en LaTeX \( \frac{3x-1}{(1+x)^3}^2 \) dentro del enunciado.<br/>",respuesta=[respuesta,respuesta2,respuesta3,respuesta4],conceptos=['demo'])
	cuestion.imagen="static/img/glyphicons-halflings.png"
	return render_template('demo.html', usuarios=usuario, grupos=grupos, cuestion=cuestion, login=current_user)

@app.route('/demof')
# class ListView(MethodView):
def demof():
	Respuesta.mas_id.set_next_value(0)

	respuesta = Respuesta(texto='respuesta de prueba',valor=-33)
	respuesta4 = Respuesta(texto='respuesta de prueba 4',valor=-33)
	# respuesta._reset_already_indexed('mas_id')
	respuesta2 = Respuesta(texto='respuesta de prueba 2',valor=100)
	respuesta3 = Respuesta(texto='\(\sqrt{3x-1}+(1+x)^2\)',valor=50)
	# cuestion = Cuestion(texto="\left [ - \frac{\hbar^2}{2 m} \frac{\partial^2}{\partial x^2} + V \right ] \Psi = i \hbar \frac{\partial}{\partial t} \Psi",respuesta=[respuesta,respuesta2,respuesta3],conceptos=['demo'])
	cuestion = Cuestion(texto=u"Enunciado con ecuaciones e imagenes de esquemas dentro de la pregunta. $$\int_a^b{x}_{0}dx $$ La cuestión puede contener ecuaciones escritas en LaTeX \( \\frac{3x-1}{(1+x)^3}^2 \) dentro del enunciado.<br/>",respuesta=[respuesta,respuesta2,respuesta3,respuesta4],conceptos=['demo'])
	cuestion.imagen = app.config['MEDIA_URL'] + 'fff.png'
	return render_template('demof.html', cuestion=cuestion)

@app.route('/listar')
def listar():
	cuestiones = Cuestion.objects.all()
	return render_template('list.html', cuestiones=cuestiones)	