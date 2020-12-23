from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # references this file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # db name here
db = SQLAlchemy(app)  # init db with app settings


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<task {self.id}>"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Error: add task failed"
    else:
        return render_template(
            "index.html", tasks=Todo.query.order_by(Todo.date_created).all()
        )


@app.route("/delete/<int:id>")
def delete(id):
    try:
        db.session.delete(Todo.query.get_or_404(id))
        db.session.commit()
        return redirect("/")
    except:
        return "Error: delete task failed"


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    tmp = Todo.query.get_or_404(id)
    if request.method == "POST":
        tmp.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Error: update task failed"
    else:
        return render_template("update.html", task=tmp)


if __name__ == "__main__":
    app.run(debug=True)