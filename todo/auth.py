import functools #Modulo para facilitar el uso de funciones y otros invocables
from flask import Blueprint, flash, g, render_template, request, url_for, session, redirect
#De flask importamos Blueprints para hacer plantillas de codigo, flash para mandar un mensaje generico
#g para acceder a variables de en este caso, db. render_templates para las plantillas html
#request para hacer pedidos al servidor, url_for para crear urls hacia los templates, session para mantener al usuario, y redirect para redireccionar
from werkzeug.security import check_password_hash, generate_password_hash
from . db import get_db

#creamos la blueprint con nombre de auth, tendra el nombre del archivo y un prefijo de /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

#al ser blueprint, se pone bp.rout en vez de app.route
@bp.route('/register', methods=['GET','POST'])
#funcion de registro
def register():
    #si el metodo es POST se pedira un usuario y contraseña
    if request.method == 'POST':
        username = request.form['username']
        password= request.form['password']
        #invocamos a la db
        db,c = get_db()
        #seteamos el valor inicial de error como None
        error = None
        #ejecutamos el cursor para ver si hay algun error
        c.execute(
            'SELECT id FROM USER WHERE username = %s', (username,)
        )
        #si no existe user o pass en el form, se lo pedirá
        if not username:
            error='Username es requerido'
        if not password:
            error = 'Password es requerido'
        #aca con el cursor buscamos el usuario, y si existe te saldra un aviso
        elif c.fetchone() is not None:
            error=f'Usuario {username} se encuentra registrado'
        
        #si no hay error, se procede a la creacion del usuario
        if error is None:
            c.execute(
                'INSERT INTO USER (username, password) VALUES (%s, %s)',
                #se encripta el password para que un hacker no lo vea normal en la db
                (username,generate_password_hash(password))
            )
            db.commit()

            #una vez registrado, te redirecciona al login
            return redirect(url_for('auth.login'))

        #si existe error, flash te muestra el error
        flash(error)
    return render_template('auth/register.html')

#ruta de Login
@bp.route('/login', methods=['GET','POST'])
#funcion Login
def login():
    #si el metodo es POST se procede al login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None

        #buscamos en la db al usuario
        c.execute (
            'SELECT * FROM USER WHERE username = %s', (username,)
        )
        #hacemos una peticion a la db para llamar los datos del usuario
        user = c.fetchone()

        #si no existe el usuario, no loguea
        if user is None:
            error= 'Usuario y/o contraseña invalida'
        #si el password esta mal, no loguea
        elif not check_password_hash(user['password'], password):
            error= 'Usuario y/o contraseña invalida'

        #en caso de que todo este en orden, se loguea segun id y se redirecciona al index
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        #si hay error, flash mandara el mensaje
        flash(error)

    #Si el metodo no es POST te reenvia a login
    return render_template('auth/login.html')

