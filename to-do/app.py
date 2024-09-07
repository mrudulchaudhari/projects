from zoneinfo import ZoneInfo
from flask import Flask, render_template # type: ignore
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

indian_time = datetime.now(ZoneInfo("Asia/Kolkata"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///todo.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default = indian_time)

    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/')

def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
