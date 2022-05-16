from dashboard import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from dashboard.models import Label, User
from dashboard.forms import RegisterForm, LoginForm, AddLabelForm, UpdateLabelForm
from dashboard import db
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/labels/<int:user_id>')
@login_required
def labels_page(user_id):
    labels = Label.query.filter_by(owner_id=user_id)
    return render_template('labels.html', labels=labels)



# register API, handles account registration post request
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # flask invokes builder pattern
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)  # pass in password to call password setter method for encryption
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    # users will be served this page when they are directed to /register
    # pass in form as a form obj
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # query through the database and find if there is a username present
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/add_label/<int:user_id>', methods=['GET', 'POST'])
@login_required
def add_label_page(user_id):
    form = AddLabelForm()
    if form.validate_on_submit():
        label_to_create = Label(label_name=form.label_name.data,
                                owner_id=user_id)
        db.session.add(label_to_create)
        db.session.commit()
        flash(f"Label with name {label_to_create.label_name} has been created)", category='success')
        return redirect(url_for('labels_page', user_id=user_id))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a label: {err_msg}', category='danger')
    return render_template('add_label.html', form=form)


@app.route('/update_label/<int:label_id>/<int:user_id>', methods=['GET', 'POST'])
def update_label(label_id, user_id):
    form = UpdateLabelForm()
    if form.validate_on_submit():
        changed_info = Label(label_name=form.label_name.data,
                             owner_id=user_id)
        original_label = Label.query.filter_by(id=label_id).first()
        db.session.delete(original_label)
        db.session.add(changed_info)
        db.session.commit()
        flash(f"Label with name {original_label.label_name} has been changed to {changed_info.label_name}", category='success')
        return redirect(url_for('labels_page', user_id=user_id))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('update_label.html', form=form)

# @app.route('/add_student', methods=['GET', 'POST'])
# @login_required
# def add_student_page():
#     form = AddStudentForm()
#     if form.validate_on_submit():
#         student_to_create = Student(name=form.name.data,
#                                     gender=form.gender.data,
#                                     age=form.age.data,
#                                     major=form.major.data,
#                                     email=form.email.data,
#                                     studentID=form.studentID.data)
#         db.session.add(student_to_create)
#         db.session.commit()
#         flash(f"Student with ID {student_to_create.studentID} has been created)", category='success')
#         return redirect(url_for('students_page'))
#     if form.errors != {}:  # If there are not errors from the validations
#         for err_msg in form.errors.values():
#             flash(f'There was an error with creating a user: {err_msg}', category='danger')
#     return render_template('add_student.html', form=form)


# @app.route('/change_student_info/<int:student_id>', methods=['GET', 'POST'])
# # @login_required
# # def change_student_info(student_id):
# #     form = AddStudentForm()
# #     if form.validate_on_submit():
# #         changed_info = Student(name=form.name.data,
# #                                gender=form.gender.data,
# #                                age=form.age.data,
# #                                major=form.major.data,
# #                                email=form.email.data,
# #                                studentID=form.studentID.data)
# #         original_student = Student.query.filter_by(id=student_id).first()
# #         db.session.delete(original_student)
# #         db.session.add(changed_info)
# #         db.session.commit()
# #         flash(f"Student with ID {changed_info.studentID} has been changed)", category='success')
# #         return redirect(url_for('students_page'))
# #     if form.errors != {}:  # If there are not errors from the validations
# #         for err_msg in form.errors.values():
# #             flash(f'There was an error with creating a user: {err_msg}', category='danger')
# #     return render_template('change_student.html', form=form)


# @app.route('/student_roster/<int:course_id>', methods=['GET', 'POST'])
# def student_roster_page(course_id):
#     target_course = Course.query.filter_by(id=course_id).first()
#     students = target_course.takers
#     return render_template('student_roster.html', students=students)
#
#
# @app.route('/close_registration/<int:course_id>', methods=['GET', 'POST'])
# def close_registration(course_id):
#     target_course = Course.query.filter_by(id=course_id).first()
#     target_course.registration_status = "CLOSED"
#     db.session.commit()
#     return redirect(url_for('courses_page'))


@app.route('/delete_label/<int:label_id>/<int:user_id>', methods=['GET', 'POST'])
def delete_label(label_id, user_id):
    target_label = Label.query.filter_by(id=label_id).first()
    db.session.delete(target_label)
    db.session.commit()
    return redirect(url_for('labels_page', user_id=user_id))


# @app.route('/delete_student/<int:student_id>', methods=['GET', 'POST'])
# def delete_student(student_id):
#     target_student = Student.query.filter_by(id=student_id).first()
#     db.session.delete(target_student)
#     db.session.commit()
#     return redirect(url_for('students_page'))

