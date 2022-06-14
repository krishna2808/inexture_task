
from quiz import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate 


# Add Database 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://hsvloyqstihcop:d7de50ce813fa0e8c5c35d56e27b99d92a2b50261fdef007c051a9ee77647ed6@ec2-54-157-16-196.compute-1.amazonaws.com:5432/d7iqtmtl8cra5e"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#initialize the database 
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(20), nullable=True)
    is_admin = db.Column(db.String(10), nullable=True ,default='False')


    # user_relationship = db.relationship('User_history', backref= 'users' )


class Subject(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     subject_name = db.Column(db.String(200), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id' , ondelete="cascade"), nullable=False)

    question_level = db.Column(db.String(200), nullable=False)
    question = db.Column(db.String(700), nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    
     
class User_history(db.Model):
    user_history_id = db.Column(db.Integer, primary_key= True ,  nullable=False)
    
    
    user_id = db.Column(db.Integer , db.ForeignKey('users.id' , ondelete="cascade"), nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    quiz_started_date = db.Column(db.DateTime, default=datetime.utcnow)
    quiz_ended_date = db.Column(db.DateTime, default=datetime.utcnow)



    
    

