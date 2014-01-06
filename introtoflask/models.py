import datetime
import random
from flask import url_for
from introtoflask import db


    # meta = {
    #     'allow_inheritance': True,
    #     'indexes': ['-created_at', 'slug'],
    #     'ordering': ['-created_at']
    # }

class Grupo(db.Document):
    nombre = db.StringField(max_length=255, required=True, unique=True)
    horario = db.StringField(max_length=255)

class Usuario(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    # id = db.Column(db.Integer, primary_key = True)
    nombre = db.StringField(max_length=255, required=True)
    apellido = db.StringField(max_length=255, required=True)
    username = db.StringField(max_length=60, required=True, unique=True)
    password = db.StringField(max_length=60, required=True)
    perfil = db.StringField(required=True)
    grupos = db.ListField(db.EmbeddedDocumentField('Grupo'))
    # grupos = db.ListField(db.StringField())
    grupo_id = db.ListField(db.StringField())

    # grupos = db.ReferenceField(Grupo)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # Required for administrative interface
    def __unicode__(self):
        return str(self.id)


    # grupos = db.ListField(db.ReferenceField(Grupo))

# class Grupo(db.EmbeddedDocument):
#     nombre = db.StringField(max_length=255, required=True, unique=True)
#     horario = db.StringField(max_length=255)

u = db.SequenceField(collection_name='Respuesta',sequence_name='mas_id', value_decorator=int(0), db_field='mas_id')
# print db.SequenceField(collection_name='Respuesta',sequence_name="mas_id",value_decorator=0).__dict__
# print u.__dict__
# print u.db_field
# print u.value_decorator(0)
print u.set_next_value(-1)

# print u.creation_counter
# u.creation_counter = 0
# # u.update(set__creation_counter=0)
# print u.creation_counter


class Respuesta(db.EmbeddedDocument):
    # respuesta_id = db.IntField()
    mas_id = db.SequenceField(required=True)
    texto = db.StringField(max_length=255, required=True)
    valor = db.IntField()

    # mas_id=set()
    # db.creation_counter = 0
# db['mongoengine.counters'].drop()

# Respuesta.mas_id.set_next_value(0)

class Cuestion(db.Document):
    short_id = db.SequenceField(required=True)
    texto = db.StringField(required=True, unique=True)
    imagen = db.StringField(max_length=255)
    imagen_aux = db.StringField(max_length=255)
    respuesta = db.ListField(db.EmbeddedDocumentField('Respuesta'))
    conceptos = db.ListField(db.StringField())
    creada_por = db.StringField(max_length=100)
    descripcion = db.StringField(max_length=255)