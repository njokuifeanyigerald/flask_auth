from flask import Blueprint, render_template, flash, request
from flask.helpers import url_for
# blueprint helps separete views
from flask_login import login_required, current_user
from werkzeug.utils import redirect
views = Blueprint('views', __name__)
from . import db
from .models import Note

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    note = Note.query.all()
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 10:
            flash ('note is too short', category= 'error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note successfully added', category='success')
            return redirect(url_for('views.home'))


    
    return render_template('home.html', user=current_user)