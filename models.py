from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(10), nullable=True)
    batch = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(30), default='IPCC')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def display_name(self):
        parts = [self.name]
        if self.section:
            parts.append(self.section)
        if self.batch:
            parts.append(f'Batch {self.batch}')
        return ' - '.join(parts)

    def __repr__(self):
        return f'{self.name} ({self.code})'


student_subject = db.Table('student_subject',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subjects = db.relationship('Subject', secondary=student_subject, lazy='subquery',
                               backref=db.backref('students', lazy=True))

    def __repr__(self):
        return f'{self.name} ({self.roll_number})'


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # Present / Absent

    student = db.relationship('Student', backref=db.backref('attendance_records', lazy=True))
    subject = db.relationship('Subject', backref=db.backref('attendance_records', lazy=True))

    __table_args__ = (db.UniqueConstraint('student_id', 'subject_id', 'date'),)

    def __repr__(self):
        return f'{self.student.name} - {self.subject.name} - {self.date} - {self.status}'


class CIE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    exam_type = db.Column(db.String(20), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    max_marks = db.Column(db.Float, default=50.0)

    student = db.relationship('Student', backref=db.backref('cie_records', lazy=True))
    subject = db.relationship('Subject', backref=db.backref('cie_records', lazy=True))

    __table_args__ = (db.UniqueConstraint('student_id', 'subject_id', 'exam_type'),)

    def __repr__(self):
        return f'{self.student.name} - {self.subject.name} - {self.exam_type}: {self.marks}/{self.max_marks}'
