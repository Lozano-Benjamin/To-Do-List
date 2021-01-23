import mariadb #modulo para usar la base de datos
import click #Herramienta para agregar y ejecutar comandos en la terminal
from . schema import instructions #Instrucciones para la db
from flask import current_app,g #Importamos los datos de la app y la var g
from flask.cli import with_appcontext #Vamos a necesitar el contexto de la app(host,usuario,contraseña,etc)

#con esta funcion conseguimos los datos de la db
def get_db():
    if 'db' not in g:
        g.db= mariadb.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c=g.db.cursor(dictionary=True)
    return g.db,g.c

#funcion que le pasaremos a init para cerrar la db
def close_db(e=None):
    db= g.pop('db',None)

    if db is not None:
        db.close()

#esta funcion recibira la app de Flask la cual ejecutara la funcion cuando
#terminemos la ejecucion de algun metodo que hayamos llamado o endpoint que creamos
def init_app(app):
    app.teardown_appcontext(close_db)