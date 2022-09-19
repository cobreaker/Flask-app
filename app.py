
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy






app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    status = db.Column(db.Boolean)


db.create_all()


@app.route('/')
def Home():
    list1 = Todo.query.all()
    return render_template('todo.html', todo_list=list1)
@app.route('/add' , methods=["POST"])
def add():
    task = request.form.get("task")
    new_todo = Todo(task=task, status=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("Home"))

@app.route("/finished/<int:todo_id>")
def finished(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.status = not todo.status
    db.session.commit()
    return redirect(url_for("list"))



@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("list"))





@app.route('/list')
def list():
    list1 = Todo.query.all()
    return render_template('list.html', todo_list=list1)

