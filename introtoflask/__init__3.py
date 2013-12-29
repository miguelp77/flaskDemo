from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "myDataBase"}
app.config["SECRET_KEY"] = "secureKey"

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()
