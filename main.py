from flask import Flask  
from flask import render_template, request, url_for, redirect
from flaskwebgui import FlaskUI
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# initialise the database
app.config['SECRET_KEY'] = 'somepassword'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportsgui.sqlite3'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = True
# creating database intsance
db = SQLAlchemy(app)

# create the db tables
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    student = db.relationship('Student', backref='project')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    result = db.relationship('Score', backref='pupil')

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

db.create_all()


@app.route("/")
def hello():  
    return render_template('landingpage.html')

@app.route("/home", methods=['GET'])
def home(): 
    return render_template('homepage.html')

@app.route("/newEvent", methods=['GET', 'POST'])
def new_project():
    if request.method == 'GET':
        return render_template('newEvent.html')
    else:
        project = request.form['session_name']
        student1 = request.form['student1']
        student2 = request.form['student2']
        student3 = request.form['student3']

        project_name = Project(
            name = project,
            date = datetime.now(),
        )
        db.session.add(project_name)
        db.session.commit()

        new_student = Student(
            name = student1,
            project = project_name,
        )
        db.session.add(new_student)
        db.session.commit()

        new_student = Student(
            name = student2,
            project = project_name,
        )
        db.session.add(new_student)
        db.session.commit()

        new_student = Student(
            name = student3,
            project = project_name,
        )
        db.session.add(new_student)
        db.session.commit()



        message = "New project created!"

        return render_template('homepage.html', message=message)


if __name__ == "__main__":

    debug = False

    if debug:
        app.run(debug=True)
    else:
        FlaskUI(app, width=500, height=500, start_server="flask").run() 
    
   