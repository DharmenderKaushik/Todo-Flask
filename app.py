from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id =   db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean,default = False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    todo_result = Todo.query.all()
    return render_template('base.html', todo_result = todo_result)

@app.route('/add',methods=['POST'])
def add():
    name = request.form.get("name")
    new_task =Todo(name = name)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<id>")
def update(id):
    task = Todo.query.get(id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<id>")
def delete(id):
    task = Todo.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)


    