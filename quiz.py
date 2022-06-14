
from flask import Flask, render_template, request , flash, redirect, url_for, session, g,flash

from forms import * 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'krishna hu mai'

app.config['UPLOAD_FOLDER'] = 'static/images/'


from modules import *


@app.before_request
def before_request():
    g.user_name = None
    if 'user_name' in session:
        g.user_name = session['user_name']


@app.route('/', methods = ['GET', 'POST'])
@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    form = Registraion()
    print(form)
    success = None 
    if request.method == 'POST': 
       print(' in post ')
       
       print(form.user_name.data, form.mobile_number.data, form.password.data,  form.submit.data, form.validate_on_submit())
       if form.validate_on_submit():
            user = Users.query.filter_by(user_name=form.user_name.data).first()
            if(user == None):
                user = Users(user_name=form.user_name.data, mobile_number=form.mobile_number.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
               
                flash('Your account successfully created')
                return redirect(url_for('log_in'))
            else:
                flash('User Name is already exist')

                success = 'User Name is already exist'
   
       form.user_name.data  = ''
       form.password.data = ''
       form.mobile_number.data = ''    
       form.submit.data = ''

    return render_template('registration.html', form=form)

# Read data from database of table 



@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = Login()
    if request.method == 'POST':
        
        print(form.user_name.data, form.password.data)
        if form.validate_on_submit():
            session.pop('user_name', None)
            user = Users.query.filter_by(user_name=form.user_name.data, password=form.password.data).first()
            if user: 
                session['user_name'] = form.user_name.data 
                if user.is_admin == 'True':
                    # return render_template('admin.html')
                    return redirect('admin_dashboard')
                elif user.is_admin == 'False':
                    return redirect('user_dashboard')
                    return render_template('dashboard.html')              
            flash('Enter valid username or password ')       

    return render_template('login.html', form=form)                

@app.route('/log_out')
def log_out():
    session["user_name"] = None 
    return redirect(url_for('log_in'))



@app.route("/show_user_data")
def show_user_data(): 
    if g.user_name: 
    # user_data = Users.query.all()

        user_data = Users.query.filter_by(is_admin='False')
        if user_data:
             return render_template('show_user_data.html', user_data=user_data, user_available =True)
        return render_template('show_user_data.html', user_available=False)
    return redirect('log_in')    


@app.route('/update_and_delete/<int:id>')
def update_and_delete(id):
    return render_template('delete_and_update_user.html', id=id)

# Update user details 

@app.route("/update/<int:id>", methods = ["POST", "GET"])
def update(id):
     form = Registraion()
     update_user =  Users.query.get_or_404(id)
    #  update_user =  Users.query.filter(id=id)

     if request.method == "POST":
        update_user.user_name = request.form['user_name']
        update_user.mobile_number = request.form['mobile_number']

        try: 
            db.session.commit()
            flash("User updated successfully ")
            return 'updated page '
            # return redirect(url_for('show_data'))


        except:
            return 'this is error page'
        return 'this page updated'     

     return render_template('update_data.html', form=form, update_user=update_user )


@app.route('/delete/<int:id>')
def delete(id):
    print('id *********** : ', id)
    user_delete = Users.query.get_or_404(id)
   
    print('User delete *********** : ', user_delete)

    try:
        db.session.delete(user_delete)
        db.session.commit()
        print('User delete ***************************  ')
        flash("user deleted ")
        return 'data deleted'
    except:
        flash("Error invalid user id ")
        print('Except ****************  ')
    return 'data not deleted'


@app.route('/subject_panel')
def subject_panel():
    return render_template('subject_panel.html')    

@app.route('/question_panel')
def question_panel():
    return render_template('question_panel.html')  


@app.route('/add_subject', methods= ['GET', 'POST'])
def add_subject():
    subject_form = SubjectForm()
    if request.method == 'POST':
        if subject_form.validate_on_submit():
            subject_name = subject_form.subject_name.data
            subject = Subject(subject_name=subject_name.upper())
            db.session.add(subject)
            db.session.commit()
            return redirect(url_for('add_subject'))

    return render_template('add_subject.html', subject_form=subject_form)    



@app.route('/update_subject', methods= ['GET', 'POST'])
def update_subject():
    subjects =  Subject.query.all()
    if len(subjects) != 0 : 
        if request.method == 'POST':
            select_subject_name = request.form.get('subject_name')
            update_subject_name = request.form.get('update_subject_name').upper()
            is_subject_available = Subject.query.filter_by(subject_name=update_subject_name).first()
            if is_subject_available == None: 
                subject_update =  Subject.query.filter_by(subject_name=select_subject_name).first()
                try:
                    subject_update.subject_name = update_subject_name
                    db.session.add(subject_update)
                    db.session.commit()
                    flash('Subject name has Updated')
                    return redirect('update_subject')
                except:
                    flash('Subject name has not updated')
                return 'subject not updated'
            else:
                return 'subject already available '         
    else:
        return redirect(url_for('admin_panel'))
                
    return render_template('update_subject.html', subjects=subjects)

            
@app.route('/delete_subject', methods = ['POST', 'GET'])
def delete_subject():
    if g.user_name: 
        subjects =  Subject.query.all()
        if len(subjects) != 0 : 

            if request.method == 'POST':
                select_subject_name = request.form.get('subject_name')
                subject_delete =  Subject.query.filter_by(subject_name=select_subject_name).first()
                try:
                    db.session.delete(subject_delete)
                    db.session.commit()

                    flash('Subject name has deleted')
                except:
                    flash("Subject name has not deleted ")
                    
                return 'subject not deleted'
        else:
            return redirect(url_for('admin_panel'))
                    
        return render_template('delete_subject.html', subjects=subjects)
    return redirect(url_for('log_in'))     


@app.route('/add_question', methods= ['GET', 'POST'])
def add_question():
    if g.user_name: 
        question_form = QuestionForm()
        subjects = Subject.query.all()
        if len(subjects) != 0 :
            question_form.select_subject.choices = []
            count = 0 
            for subject in subjects: 
                question_form.select_subject.choices.append(( str(count), subject.subject_name))
                count += 1 

            if request.method == 'POST':
                if question_form.validate_on_submit():
                    question = question_form.question.data.lower()
                    option1 = question_form.option1.data.lower()
                    option2 = question_form.option2.data.lower()
                    option3 = question_form.option3.data.lower()
                    option4 = question_form.option4.data.lower()
                    answer = question_form.answer.data.lower()
                    option_set = {option1, option2, option3, option4}
                    if len(option_set) == 4 and answer in option_set:
                        select_subject = question_form.select_subject.choices[question_form.select_subject.data][1]
                        question_level = question_form.select_question_level.choices[question_form.select_question_level.data][1]
                        subject_id = Subject.query.filter_by(subject_name=select_subject).first().id
                        question_table = Question(subject_id= subject_id, question_level=question_level , question=question, option1=option1, option2=option2, option3=option3, option4=option4, answer=answer)
                        db.session.add(question_table)
                        db.session.commit()
                        flash('Question is added successfully')
                        
                    
                    return redirect(url_for('add_question'))    
        return render_template('add_question.html', question_form=question_form)  
    return redirect(url_for(log_in))    

                
@app.route('/user_dashboard')
def user_dashboard():
    if g.user_name: 
        return render_template('user_dashboard.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if g.user_name:
        flash('Welcome to Admin panel')
        return render_template('admin_dashboard.html')
    return redirect(url_for('log_in'))    

@app.route('/choice_subject_and_question_level', methods = ['POST', 'GET'])
def choice_subject_and_question_level():
    if g.user_name: 
        subjects = Subject.query.all()
        question = Question.query.all()
        if(len(subjects) !=0 and len(question) !=0 ):
            if request.method == 'POST':
                select_subject_name = request.form.get('subject_name')
                question_level = request.form.get('question_level')
                subject_name  = Subject.query.filter_by(subject_name=select_subject_name).first()
                subject_id = subject_name.id
                print('*******************8', select_subject_name,'******', question_level, subject_id)
                return redirect(url_for('quiz_start', question_level=question_level, subject_name=select_subject_name))

        else:
            return 'data is not available ' 
        return render_template('question_level_and_subject.html', subjects=subjects) 
    return redirect(url_for('log_in'))              




# @app.route('/quiz_start', methods= ['GET', 'POST'])
@app.route('/quiz_start/<question_level>/<subject_name>', methods = ['POST', 'GET'])
def quiz_start(question_level, subject_name):
    if g.user_name: 
        subject_name  = Subject.query.filter_by(subject_name=subject_name).first()
        subject_id = subject_name.id
        questions = Question.query.filter_by(subject_id=subject_id, question_level=question_level)
        print('this is ******** ')
        if request.method == 'POST':
            lst = []
            for question in questions:
                choice_option = request.form[question.id]
                lst.append(choice_option)
            return f'lst ***  {lst}'    


        return render_template('quiz_start.html', questions=questions)  
    return redirect(url_for('log_in'))    
