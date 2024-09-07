from zoneinfo import ZoneInfo
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))

    def __repr__(self):
        return f'<Todo {self.id}: {self.task}>'

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    print("Todos retrieved:", todos)  # Debugging print
    for todo in todos:
        print(f"ID: {todo.id}, Task: {todo.task}, Completed: {todo.completed}, Created At: {todo.created_at}")
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    if task:
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        print(f"Added new todo: {new_todo}")  # Debugging print
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    print(f"Toggled completion for todo {id}: {todo.completed}")  # Debugging print
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    print(f"Deleted todo {id}")  # Debugging print
    return redirect(url_for('index'))

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized")  # Debugging print

if __name__ == '__main__':
    init_db()
    app.run(debug=True)