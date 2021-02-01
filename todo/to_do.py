from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp=Blueprint('to_do',__name__)

#muestra los to do, tambien es el index
@bp.route('/')
@login_required
def index():
    #LLama a la funcion para llamar a la db, despues de eso ejecuta el cursor pidiendo datos, ordenando por la fecha y descripcion
    db, cursor = get_db()
    cursor.execute(
        'SELECT T.id, T.description, U.username, T.completed, T.created_at FROM TODO T JOIN USER U ON T.created_by = U.id WHERE T.created_by = %s ORDER BY created_at desc',
        (g.user['id'],)
        
    )

    #invoca a todos los datos encontrados
    to_dos= cursor.fetchall()
    
    #devuelve la plantilla index
    return render_template('todo/index.html', to_dos=to_dos)

#crear un to do
@bp.route('/create', methods=['GET', 'POST'])
@login_required
#Funcion para crear los to do
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error='Descripcion es requerida'
        
        if error is not None:
            flash(error)
        else:
            db,cursor=get_db()
            cursor.execute(
                'INSERT INTO TODO(description, completed, created_by)'
                'VALUES ( %s, %s, %s)',
                (description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('to_do.index'))
    return render_template('todo/create.html')

def get_todo(id):
    db, c = get_db()
    c.execute(
        'SELECT T.id, T.description, T.completed, T.created_by, T.created_at, U.username '
        'FROM TODO T JOIN USER U ON T.created_by = U.id WHERE T.id = %s',
        (id,)
    )

    todo = c.fetchone()

    if todo is None:
        abort(404, "El To Do de id {0} no existe".format(id))
    
    return todo

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo= get_todo(id)

    if request.method == 'POST':
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        error= None 

        if not description:
            error = "La descripcion es requerida."
        
        if error is not None:
            flash(error)
        
        else:
            db, cursor = get_db()
            cursor.execute(
                "UPDATE TODO SET description = %s, completed = %s WHERE id = %s and created_by= %s",
                (description, completed, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('to_do.index'))
    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute('DELETE FROM TODO WHERE id= %s and created_by = %s',(id, g.user['id']))
    db.commit()
    return redirect(url_for('to_do.index'))