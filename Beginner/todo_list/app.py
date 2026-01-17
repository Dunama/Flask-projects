from config import create_app
from routes.routes import todo_bp
from tests.tests import test_bp

app = create_app()

app.register_blueprint(todo_bp)
app.register_blueprint(test_bp)


if __name__ == '__main__':
    app.run(debug=True)