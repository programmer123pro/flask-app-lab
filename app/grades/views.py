from flask import *
from sqlalchemy import and_
from . import grades_bp
from .forms import GradeForm
from .models import *
from flask_login import login_required

@grades_bp.route('/add_grade', methods=['GET', 'POST'])
@login_required
def add_grade():
    form = GradeForm()
    groups = list(set([group[0] for group in db.session.query(Student).with_entities(Student.group).all()]))
    form.setGroupList(groups)
    subjects = db.session.query(Subject).all()
    form.setSubjectList(subjects)

    if(request.method == 'GET'):
        return render_template('add_grade.html', form=form, title='Додати нову оцінку')
    
    elif(request.method == 'POST'):
        if form.validate_on_submit():
            group = form.student_group.data
            name = form.student_name.data
            surname = form.student_surname.data
            student = db.session.query(Student).filter(and_(Student.group == group, Student.name == name, Student.surname == surname)).all()
            subject_id = form.subject.data
            grade = form.grade.data
            if student and subject_id:
                student = student[0]
                exist_grade = Grade.query.filter(and_(Grade.student_id == student.id, Grade.subject_id == subject_id)).all()
                if exist_grade:
                    exist_grade[0].grade = grade
                else:
                    new_grade = Grade(student=student, subject_id=subject_id, grade=grade)
                    db.session.add(new_grade)
                db.session.commit()
                flash("Оцінку успішно додано!", "success")
            else:
                flash("Такого студента не існує!", "warning")
            return redirect(url_for('.add_grade'))
        else:
            return render_template('add_grade.html', form=form, title='Додати нову оцінку')

@grades_bp.route("all_grades")
def view_all():      
    if 'sort' in request.args:
        sort = request.args['sort']
        if(sort == 'За прізвищем'):
            grades = Grade.query.join(Student).order_by(Student.surname).all()
        elif(sort == 'За предметом'):
            grades = Grade.query.join(Subject).order_by(Subject.name).all()
        elif(sort == 'За оцінкою'):
            grades = Grade.query.order_by(Grade.grade).all()
    else:
        grades = Grade.query.all()

    gradeDicts = [] 
    for g in grades:
        gradeDicts.append({
            'student' : (g.student.name+' '+g.student.surname),
            'subject' : g.subject.name,
            'grade' : g.grade
        })
    sorts = ["За прізвищем", "За предметом", "За оцінкою"]

    return render_template('all_grades.html', grades=gradeDicts, sorts=sorts)

@grades_bp.route('/student_grades/<int:id>')
def view_student(id):
    student = Student.query.get_or_404(id)
    return render_template('view_student_grades.html', student=student)

@grades_bp.route('/edit_grade/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    grade = Grade.query.get_or_404(id)
    form = GradeForm()
    groups = list(set([group[0] for group in db.session.query(Student).with_entities(Student.group).all()]))
    form.setGroupList(groups)
    subjects = db.session.query(Subject).all()
    form.setSubjectList(subjects)

    if(request.method == 'GET'):
        form.student_group.data = grade.student.group
        form.student_name.data = grade.student.name
        form.student_surname.data = grade.student.surname
        form.subject.data = grade.subject.id
        form.grade.data = grade.grade
        return render_template('add_grade.html', form=form, title='Редагувати оцінку')
    
    elif(request.method == 'POST'):
        if form.validate_on_submit():
            group = form.student_group.data
            name = form.student_name.data
            surname = form.student_surname.data
            student = db.session.query(Student).filter(and_(Student.group == group, Student.name == name, Student.surname == surname)).all()
            subject_id = form.subject.data
            mark = form.grade.data
            if student:
                grade.student = student[0]
                grade.subject_id = subject_id
                grade.grade = mark
                db.session.commit()
                flash('Оцінка успішно оновлена!', 'success')
            else:
                flash("Такого студента не існує!", "warning")
            return redirect(url_for('.view_student', id=grade.student.id))
        return render_template('add_grade.html', form=form, title='Редагувати оцінку')

@grades_bp.route('/delete_grade/<int:id>')
@login_required
def delete(id):
    grade = Grade.query.get_or_404(id)
    student_id = grade.student.id
    db.session.delete(grade)
    db.session.commit()
    flash('Оцінку успішно видалено!', 'success')
    return redirect(url_for('.view_student', id=student_id))
    