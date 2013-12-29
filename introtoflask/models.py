import datetime
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

class Respuesta(db.EmbeddedDocument):
    respuesta_id = db.IntField()
    texto = db.StringField(max_length=255, required=True)
    valor = db.IntField()


class Cuestion(db.Document):
    cuestion_id = db.IntField()
    texto = db.StringField(required=True, unique=True)
    imagen = db.StringField(max_length=255)
    imagen_aux = db.StringField(max_length=255)
    respuesta = db.ListField(db.EmbeddedDocumentField('Respuesta'))
    conceptos = db.ListField(db.StringField())    
