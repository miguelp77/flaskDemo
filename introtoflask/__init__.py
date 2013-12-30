# -*- coding: utf-8 -*-
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

from flask.ext.principal import Principal, Permission, RoleNeed

app = Flask(__name__)     

app.jinja_env.add_extension('jinja2.ext.do')

app.config["MONGODB_SETTINGS"] = {'DB': "myDataBase"}
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# app.config["DEBUG_TB_PANELS"] = {'flask.ext.mongoengine.panels.MongoDebugPanel'}
app.config["DEBUG_TB_PANELS"] = [
	'flask_debugtoolbar.panels.versions.VersionDebugPanel',
	'flask_debugtoolbar.panels.timer.TimerDebugPanel',
	'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
	'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
	'flask_debugtoolbar.panels.template.TemplateDebugPanel',
	'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
	'flask_debugtoolbar.panels.logger.LoggingPanel',
	'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        # Add the MongoDB panel
	'flask_debugtoolbar_mongo.panel.MongoDebugPanel',
	]

app.secret_key = 'secureKey'
app.config["SECRET_KEY"] = "secureKey"
app.debug=True


db = MongoEngine(app)
# tool = DebugToolbarExtension(app)


principals = Principal(app)
normal_role = RoleNeed('normal')
normal_permission = Permission(normal_role)
admin_role = RoleNeed('admin')
admin_permission = Permission(admin_role)
principals._init_app(app)

# # User Information providers
# @identity_loaded.connect_via(app)
# def on_identity_loaded(sender, identity):
#     user = Usuario.objects.get(perfil=identity)


lm = LoginManager()
lm.login_view = "login"
lm.login_message = u"Es necesario que este registrado para acceder."
lm.init_app(app)



def register_blueprints(app):
    # Prevents circular imports
    from introtoflask.manage import usuarios
    from introtoflask.main_ops import main_operations
    from introtoflask.preguntas_ops import preguntas_ops
    app.register_blueprint(usuarios)
    app.register_blueprint(main_operations)
    app.register_blueprint(preguntas_ops)

register_blueprints(app)

import introtoflask.manage