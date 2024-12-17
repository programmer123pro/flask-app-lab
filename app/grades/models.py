from app import db
from datetime import datetime as dt
from sqlalchemy.orm import backref

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    student = db.relationship('Student')
    subject = db.relationship('Subject', lazy="joined")


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    group = db.Column(db.String(20), nullable=False)
    
    grades = db.relationship('Grade', back_populates="student")

    def __repr__(self):
        return f"{self.name} {self.surname}"


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return self.name

