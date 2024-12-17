from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import *
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt

def gradeValidate(form, field):
    if field.data < 0 or field.data > 10:
        raise ValidationError('Оцінка повинна бути від 0 до 10!')

class GradeForm(FlaskForm):
    student_group = SelectField("Група:", coerce=str, validators=[DataRequired()])
    student_name = StringField("Ім'я:", validators=[DataRequired()])
    student_surname = StringField("Прізвище:", validators=[DataRequired()])
    subject = SelectField("Предмет:", coerce=int, validators=[DataRequired()])
    grade = IntegerField("Оцінка:", validators=[DataRequired(), gradeValidate])
    submit = SubmitField('Додати оцінку')

    def setSubjectList(self, subjects):
        self.subject.choices = [(subject.id, subject.name) for subject in subjects]

    def setGroupList(self, groups):
        self.student_group.choices = groups