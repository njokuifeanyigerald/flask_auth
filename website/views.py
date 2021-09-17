from flask import Blueprint, render_template, flash, request
from flask.helpers import url_for
# blueprint helps separete views
from flask_login import login_required, current_user
from werkzeug.utils import redirect
views = Blueprint('views', __name__)
from . import db
from .models import Note
from sqlalchemy import desc

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    # for reference purpose
    # there are 2 method to pull data from the current user either this way or 
    # the 'user.note' way which works with current_user which will be added to the home.html
    my_notes = Note.query.filter_by(user_id=current_user.id).order_by(desc(Note.date))
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
    return render_template('home.html', user=current_user, my_notes=my_notes)