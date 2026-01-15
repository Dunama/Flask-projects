from config import create_app
from tests.tests import test_bp
from routes.routes import contact_bp


app = create_app()

app.register_blueprint(test_bp)
app.register_blueprint(contact_bp)


if __name__ == '__main__':
    app.run(debug=True)