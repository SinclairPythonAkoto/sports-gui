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

# create all db tables
db.create_all()


# db table functions
def create_new_project(proj_name):
    """
    Creates a new project, storing it in the Project db table.
    Returns the Project object after saving it.
    """
    with app.app_context():
        new_project = Project(
            name = proj_name,
            date = datetime.now(),
        )
        db.session.add(new_project)
        db.session.commit()
    return new_project

def create_new_student(student_name, usr_project):
    """
    Creates a new student, storing it in the Student db table.
    Returns the Student object after saving it.
    """
    with app.app_context():
        new_student = Student(
            name = student_name,
            project = usr_project,
        )
        db.session.add(new_student)
        db.session.commit()
    return new_student

def add_new_score(student_score, student_notes, student):
    """
    Creates a new score, storing it into the Score db table.
    Returns the Score object after saving it.
    """
    with app.app_context():
        new_score = Score(
            Score = student_score,
            notes = student_notes.lower(),
            date = datetime.now(),
            pupil = student,
        )
        db.session.add(new_score)
        db.session.commit()
    return new_score


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
    
   