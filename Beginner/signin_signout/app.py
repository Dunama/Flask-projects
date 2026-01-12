from flask_login import LoginManager
from config import create_app, db
from models.models import User
from routes.routes import auth_bp
from tests.tests import test_bp

app = create_app()

login_manager = LoginManager()
login_manager.login_view = 'auth_bp.signin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	'''load user by ID'''
	return User.query.get(int(user_id))

# Register Blueprints From Routes
app.register_blueprint(auth_bp)
app.register_blueprint(test_bp, url_prefix='/test')




if __name__ == '__main__':
	app.run(debug=True)