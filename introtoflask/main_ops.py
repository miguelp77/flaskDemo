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
	user = current_user
	return render_template('home.html',user=user)

@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/_ajax')
def devuelvo():
	user_id = request.args.get('a')
	user =Usuario.objects.get(id=user_id).to_json()
	# print(user.__dict__)
	b=json_util.dumps(user)
	# b= user.username
	# user.delete()
	return user
	# return jsonify(result= b)
	# return jsonify(result= b)

@app.route('/_addGroup')
def addGroup():
	user_id = request.args.get('a')
	usuario =Usuario.objects.get(id=user_id).to_json()
	# grupo=Grupo(nombre="test1",horario="L-M  10:00-12:00")
	# usuario.grupos.update_one(push__grupos=grupo)
	
	# user = Usuario.objects.get(id=user_id)
	# if uniqueName(user_id,"test1"):
	# 	user.update(push__grupos=grupo)
	# 	user.save()

	# Eliminar un grupo con update y pull
	# Usuario.objects.get(id=user_id).update(pull__grupos__nombre='test1')
	# gs = Usuario.objects(Q(grupos__nombre__exists=True))[:1]
	# gs = []
	# for u in Usuario.objects(Q(grupos__exists=True)):
	# 	g = u.grupos[0].nombre
	# 	if not (g in gs):
	# 		gs.append(g)
	
	# print ', '.join(gs)
	# return ', '.join(gs)
	# return usuario

@app.route('/_addGroupToUser')
def addGroupToUser():
	print "OOOO"
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
	user_id = request.args.get('u')
	grupo_id = request.args.get('g')
	# usuario =Usuario.objects.get(id=user_id).to_json()
	# grupo=Grupo(nombre="test3",horario="L-M  10:00-12:00")
	# usuario.grupos.update_one(push__grupos=grupo)
	
	# user = Usuario.objects.get(id=user_id)
	# if uniqueName(user_id,"test3"):
	# 	user.update(push__grupos=grupo)
	# 	user.save()
	
	# Eliminar un grupo con update y pull
	usuario = Usuario.objects.get(id=user_id).update(pull__grupos__id=grupo_id)

	return "Removed"

# def listGroups():


def uniqueName(user_id,name):
	grupo = Usuario.objects(id=user_id, grupos__nombre__iexact=nombre)
	# grupo = Grupo.objects.get(nombre__iexact=name)
	if len(grupo) > 0:
		return False
	return True
