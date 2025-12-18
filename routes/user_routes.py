from flask import Blueprint, render_template, request, redirect, url_for
from models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form.get('gender')
        User.create(name=name, gender=gender)
        return redirect(url_for('user.index'))
    
    users = User.select()
    return render_template('user_list.html', users=users)