from flask import Blueprint, render_template, redirect, url_for
from models.models import TodoList
from forms.forms import TodoForm
from config import db

todo_bp = Blueprint('todo_bp', __name__)

@todo_bp.route('/', methods=['GET'])
def home():
    return redirect(url_for('todo_bp.post_todo'))

@todo_bp.route('/todos', methods=['GET', 'POST'])
def post_todo():
    form = TodoForm()

    if form.validate_on_submit():
        todo_item = TodoList(
            title=form.title.data,
            completed=bool(form.completed.data),
        )
        db.session.add(todo_item)
        db.session.commit()
        return redirect(url_for('todo_bp.post_todo'))

    todos = TodoList.query.order_by(TodoList.created_at.desc(), TodoList.id.desc()).all()
    return render_template('todo.html', form=form, todos=todos)


@todo_bp.route('/todos/complete/<int:todo_id>', methods=['POST'])
def complete_todo(todo_id: int):
    todo = TodoList.query.get_or_404(todo_id)
    todo.completed = True
    db.session.commit()
    return redirect(url_for('todo_bp.post_todo'))


@todo_bp.route('/todos/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id: int):
    todo = TodoList.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo_bp.post_todo'))
    


