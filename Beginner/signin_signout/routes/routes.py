from forms.forms import SignInForm, SignUpForm
from models.models import User
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from config import db

auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates')
 
@auth_bp.route('/')
def index():
    '''index route'''
    return render_template('index.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    '''signup route: creating users sessions'''
    try:
        form = SignUpForm()
        if form.validate_on_submit():
            user = User(
                email=form.email.data
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            flash('Account created. Please sign in.', 'success')
            # after a succesful signin, redirect to login page
            return redirect(url_for('auth_bp.signin'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating account: {e}')

    return render_template('signup.html', form=form)


@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    '''login route: for authenticating signed up users'''
    try:
        form = SignInForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for('auth_bp.dashboard'))
            else:
                flash('Invalid email or password.')
    except Exception as e:
        flash(f'Error logging in: {e}')
    return render_template('signin.html', form=form)


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth_bp.index'))
