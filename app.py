from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)


app.secret_key = "1234abcdef"


# Create Tables
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, default=0)

    def __init__(self, title, status=0):
        self.title = title
        self.status = status

    def __repr__(self):
        return "<Todo %s" % self.title


# -CRUD-  Read + Insert
@app.route("/", methods=["GET", "POST"])
def index():
    todos = Todo.query.all()
    if request.method == "POST":
        # insert
        title = request.form['todo']
        todo = Todo(title)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("todos.html", todos=todos)


# -CRUD- Update
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == "POST":
        todo.title = request.form['todo']
        todo.status = 0
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("edit.html", todo=todo)


# -CRUD- Delete
@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/task/<int:id>/done')
def done(id):
    todo = Todo.query.get_or_404(id)
    todo.status = 1
    db.session.commit()
    return redirect(url_for('index'))


# Search
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        title = request.form['search']
        search = "%{}%".format(title)
        todos = Todo.query.filter(Todo.title.like(search)).all()

        return render_template("todos.html", todos=todos)


if __name__ == '__main__':
    app.run(debug=True)
