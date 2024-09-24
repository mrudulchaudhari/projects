from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Indian time zone
indian_tz = pytz.timezone('Asia/Kolkata')

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(indian_tz))
    completed_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, *args, **kwargs):
        super(Todo, self).__init__(*args, **kwargs)
        self.created_at = datetime.now(indian_tz)

    def __repr__(self):
        return f'<Todo {self.id}: {self.task}>'

@app.route('/')
def index():
    pending_todos = Todo.query.filter_by(completed=False).order_by(Todo.created_at.desc()).all()
    completed_todos = Todo.query.filter_by(completed=True).order_by(Todo.completed_at.desc()).all()
    return render_template('index.html', pending_todos=pending_todos, completed_todos=completed_todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    if task:
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    if todo.completed:
        todo.completed_at = datetime.now(indian_tz)
    else:
        todo.completed_at = None
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.task = request.form['task']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)