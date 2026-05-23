from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, RadioField
from wtforms.validators import DataRequired, Email

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    code = StringField('Subject Code', validators=[DataRequired()])
    section = SelectField('Section', choices=[
        ('', '---'),
        ('Theory', 'Theory'),
        ('Lab', 'Lab')
    ], default='')
    batch = StringField('Batch (e.g. 1, 2, 3)', validators=[])
    category = SelectField('Category', choices=[
        ('IPCC', 'IPCC (Theory + Lab)'),
        ('PCC', 'PCC (Only Theory)'),
        ('Department Elective', 'Department Elective'),
        ('Open Elective', 'Open Elective'),
        ('Lab', 'Lab'),
        ('Project', 'Project'),
        ('Remedial', 'Remedial')
    ], default='IPCC')
    submit = SubmitField('Save')


class StudentForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    roll_number = StringField('Roll Number', validators=[DataRequired()])
    submit = SubmitField('Save')


class AttendanceForm(FlaskForm):
    subject = SelectField('Subject', coerce=int, validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Mark Attendance')
