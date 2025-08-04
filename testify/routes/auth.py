from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from extensions import db
from models.user import User

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET'])
def index():
    if request.method == 'POST':
        return redirect(url_for('auth.landing'))
    return redirect(url_for('auth.landing'))


# @bp.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         return redirect(url_for('auth.login'))
#     return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    from models.user import User
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('auth.mode_select'))
        flash('Invalid email or password')
    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    from models.user import User
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'Viewer')
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('signup.html')
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    # return redirect(url_for('auth.login'))
    return render_template('login.html')

@bp.route('/mode_select')
@login_required
def mode_select():
    return render_template('mode_select.html')

@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        flash('Password reset instructions sent to ' + email)
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')

@bp.route('/profile', methods=['GET', 'POST'])

def profile():
    if request.method == 'POST':
        user = current_user
        user.name = request.form.get('name')
        # Add password change logic here if needed
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))
    return render_template('profile.html')


@bp.route('/landing')
def landing():
    return render_template('landing.html')