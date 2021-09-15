from flask import Blueprint, render_template
# blueprint helps separete views
from flask_login import login_required
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html')