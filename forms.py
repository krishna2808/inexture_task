# from blog import app

from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, validators, PasswordField,SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


# create form class 

class Registraion(FlaskForm):

    user_name = StringField('Username', validators=[DataRequired() , Length(min=2, max=20)])
    mobile_number = StringField('Mobile Number',  validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(),  Length(min=5, max=10)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('password', message='Passwords must match'),  Length(min=5, max=10)])
    
    submit  = SubmitField('Submit')

    
    def __repr__(self):
        return '<Username %r>' % self.user_name


class Login(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired() , Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(),  Length(min=5, max=10)])
    submit  = SubmitField('Submit')


class SubjectForm(FlaskForm):
    subject_name = StringField('Subject Name ', validators=[DataRequired(),  Length(min=6, max=25)])
    submit  = SubmitField('Submit',  validators=[DataRequired()])


class QuestionForm(FlaskForm):
    question = StringField('Question ', validators=[DataRequired()])
    select_question_level = SelectField('Question Level ', coerce=int, choices=[('0', 'Easy'), ('1', 'Medium'), ('2', 'Hard')])
    select_subject = SelectField('Select Subject ', coerce=int, choices=[('1', 'No Subject ')])

    option1 = StringField('Option 1  ', validators=[DataRequired()])
    option2 = StringField('Option 2  ', validators=[DataRequired()])
    option3 = StringField('Option 3  ', validators=[DataRequired()])
    option4 = StringField('Option 4  ', validators=[DataRequired()])
    answer = StringField('Answer ', validators=[DataRequired()])

    submit  = SubmitField('Submit',  validators=[DataRequired()])

