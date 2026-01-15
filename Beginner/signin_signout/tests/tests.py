from forms.forms import SignInForm, SignUpForm
from models.models import User
from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required
from config import db

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/')
def test_index():
    return jsonify({"message": "Test Blueprint is working!"})

@test_bp.route('/signup', methods=['POST'])
def test_signup():
    """Test signup route (JSON-friendly)"""
    try:
        form = SignUpForm(meta={"csrf": False})

        if request.is_json:
            form.process(data=request.get_json())
        else:
            form.process(formdata=request.form)

        if not form.validate():
            return jsonify({"error": "validation failed", "details": form.errors}), 400

        # optional: prevent duplicate emails
        if User.query.filter_by(email=form.email.data).first():
            return jsonify({"error": "email already exists"}), 409

        user = User(email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "account created"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating account: {e}"}), 500

@test_bp.route('/signin', methods=['POST'])
def test_signin():
    """Test signin route (JSON-friendly)"""
    try:
        form = SignInForm(meta={"csrf": False})

        if request.is_json:
            form.process(data=request.get_json())
        else:
            form.process(formdata=request.form)

        if not form.validate():
            return jsonify({"error": "validation failed", "details": form.errors}), 400

        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            return jsonify({"error": "invalid email or password"}), 401

        login_user(user)
        return jsonify({"message": "logged in"}), 200

    except Exception as e:
        return jsonify({"error": f"Error logging in: {e}"}), 500

@test_bp.route('/logout', methods=['POST'])
@login_required
def test_logout():
    '''Test logout route'''
    logout_user()
    return jsonify({"message": "logged out"}), 200


# Routes to get the number of signed-in users (for testing purposes)
@test_bp.route('/status/<int:user_id>', methods=['GET'])
def get_single_status(user_id):
    '''Get sign-in status of a single user'''
    user = User.query.get(user_id)
    if user:
        return jsonify({"user_id": user_id, "signed_in": user.is_authenticated}), 200
    else:
        return jsonify({"error": "user not found"}), 404

@test_bp.route('/status', methods=['GET'])
def get_all_status():
    '''Get sign-in status of all users'''
    users = User.query.all()
    status_list = [
        {
            "user_id": user.id,
            "email": user.email,
            "signed_in": user.is_authenticated,
        }
        for user in users
    ]
    return jsonify(status_list), 200