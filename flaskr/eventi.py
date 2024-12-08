from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('eventi', __name__)


@bp.route('/')
def index():
    db = get_db()
    eventi = db.execute(
        'SELECT p.id, title, body, created, author_id, username, event_date'
        ' FROM eventi p JOIN utenti u ON p.author_id = u.id'
        ' ORDER BY event_date DESC'
    ).fetchall()
    return render_template('eventi/index.html', eventi=eventi)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        event_date = request.form['event_date']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO eventi (title, body, author_id, event_date)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], event_date)
            )
            db.commit()
            return redirect(url_for('eventi.index'))

    return render_template('eventi/create.html')


def get_evento(id, check_author=True):
    evento = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, event_date'
        ' FROM eventi p JOIN utenti u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if evento is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and evento['author_id'] != g.user['id']:
        abort(403)

    return evento


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    evento = get_evento(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        event_date = request.form['event_date']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE eventi SET title = ?, body = ?, event_date=?'
                ' WHERE id = ?',
                (title, body, event_date, id)
            )
            db.commit()
            return redirect(url_for('eventi.index'))

    return render_template('eventi/update.html', evento=evento)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_evento(id)
    db = get_db()
    db.execute('DELETE FROM eventi WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('eventi.index'))