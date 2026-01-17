from flask import Blueprint, request, jsonify
from models.models import TodoList
from forms.forms import TodoForm
from config import db

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/', methods=['POST'])
def test():
    return jsonify({"message": "Todo List Test Blueprint is working!",
                    "status": "success"}), 200


@test_bp.route('/test', methods=['POST'])
def post_todo():
    '''Endpoint to create a new todo item for testing purposes.'''
    try:
        form = TodoForm(meta={'csrf': False})
        if request.is_json:
            form.process(data=request.get_json())
        else:
            form.process(formdata=request.form)

        if not form.validate():
            return jsonify({"error": "validation failed", "details": form.errors}), 400
        
        todo_items = TodoList(
            title=form.title.data,
            completed=form.completed.data
        )
        
        db.session.add(todo_items)
        db.session.commit()
        return jsonify({"message": "todo item created", "data": {
            "id": todo_items.id,
            "title": todo_items.title,
            "completed": todo_items.completed,
            "created_at": todo_items.created_at.isoformat()
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating todo item: {e}"}), 500


@test_bp.route('/test/all', methods=['GET'])
def get_all_todos():
    ''' Endpoint to retrieve all todo items for testing purposes. '''
    try:
        todos = TodoList.query.all()
        todos_data = [{
            "id": todo.id,
            "title": todo.title,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat()
        } for todo in todos]
        return jsonify({"todos": todos_data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error retrieving todo items: {e}"}), 500

@test_bp.route('/test/clear/<int:test_id>', methods=['DELETE'])
def clear_todos(test_id):
    ''' Endpoint to delete single todo items for testing purposes. '''
    try:
        todo = TodoList.query.get(test_id)
        if not todo:
            return jsonify({"error": "todo item not found"}), 404
        db.session.delete(todo)
        db.session.commit()  
        return jsonify({"message": "todo item deleted", "id": test_id}), 200
  
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deleting todo item: {e}"}), 500
    