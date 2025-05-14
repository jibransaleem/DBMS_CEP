from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField, SubmitField, PasswordField, SelectField , TextAreaField,DateField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileAllowed
class JobSeekerForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message="Please enter your full name"),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="Please enter your email"),
        Email(message="Please enter a valid email address")
    ])
    phone = TelField('Phone Number', validators=[
        DataRequired(message="Please enter your phone number"),
        Length(min=10, message="Please enter a valid phone number")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter a password"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Sign Up as Job Seeker')

class RecruiterForm(FlaskForm):
    # Reduced industry choices
    INDUSTRY_CHOICES = [
        ('', 'Select an industry'),
        ('technology', 'Technology & IT'),
        ('healthcare', 'Healthcare & Medical'),
        ('finance', 'Finance & Banking'),
        ('education', 'Education & Training'),
        ('retail', 'Retail & E-commerce'),
        ('manufacturing', 'Manufacturing & Production'),
        ('other', 'Other')
    ]
    
    company_name = StringField('Company Name', validators=[
        DataRequired(message="Please enter your company name"),
        Length(min=2, max=100, message="Company name must be between 2 and 100 characters")
    ])
    company_email = EmailField('Email', validators=[
        DataRequired(message="Please enter your company email"),
        Email(message="Please enter a valid email address")
    ])
    company_phone = TelField('Phone Number', validators=[
        DataRequired(message="Please enter your company phone number"),
        Length(min=10, message="Please enter a valid phone number")
    ])
    company_location = StringField('Location', validators=[
        DataRequired(message="Please enter your company location"),
        Length(min=2, max=100, message="Location must be between 2 and 100 characters")
    ])
    company_industry = SelectField('Industry', 
        choices=INDUSTRY_CHOICES,
        validators=[DataRequired(message="Please select your company industry")]
    )
    company_password = PasswordField('Password', validators=[
        DataRequired(message="Please enter a password"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    company_confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('company_password', message="Passwords must match")
    ])
    submit = SubmitField('Sign Up as Recruiter')

class Login(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message="Please enter your email"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter a password"),
    ])

    Role = SelectField('Login as', 
        choices=['Candidate', 'Company'],
        validators=[DataRequired(message="Please select your Login type")]
    )
    submit = SubmitField('Login')
class JobPostForm(FlaskForm):
    title = StringField('Job Title', validators=[
        DataRequired(), Length(min=3, max=100)
    ])
    
    description = TextAreaField('Job Description', validators=[
        DataRequired(), Length(min=10)
    ])
    qualification = TextAreaField('Job Qualification', validators=[
        DataRequired(), Length(min=10)
    ])

    location = StringField('Job Location', validators=[
        DataRequired(), Length(min=2, max=100)
    ])

    city = StringField('Job City', validators=[
        DataRequired(), Length(min=2, max=100)
    ])

    job_type = SelectField('Job Type', choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Trainee', 'Trainee'),
        ('Internship', 'Internship'),
    ], validators=[DataRequired()])

    SALARY_CHOICES = [
    ('Below 30,000', 'Below 30,000'),
    ('30,000 - 50,000', '30,000 - 50,000'),
    ('50,000 - 70,000', '50,000 - 70,000'),
    ('70,000 - 100,000', '70,000 - 100,000'),
    ('Above 100,000', 'Above 100,000'),
]
    salary = SelectField('Salary Range', choices=SALARY_CHOICES, validators=[DataRequired()])
    skills = StringField('Skills Required', validators=[
        DataRequired(), Length(min=2)
    ])
    job_industry = SelectField(
        'Job Industry',
        choices=[
            ("technology", "Technology"),
            ("healthcare", "Healthcare"),
            ("finance", "Finance"),
            ("education", "Education"),
            ("retail", "Retail"),
            ("manufacturing", "Manufacturing"),
            ("other", "Other")
        ],
        validators=[DataRequired()]
    )
    job_status = SelectField(
        'Job Status',
        choices=[('open', 'Open'), ('closed', 'Closed')],
        validators=[DataRequired()]
    )
    
    dead_line = DateField(
        'Application Deadline',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Post Job')
class JobApplicationForm(FlaskForm):
    resume = FileField('Upload Resume', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'], 'Documents only!')])
    submit = SubmitField('Submit Application')
    
class Edit_Company(FlaskForm) :
    INDUSTRY_CHOICES = [
        ('', 'Select an industry'),
        ('technology', 'Technology & IT'),
        ('healthcare', 'Healthcare & Medical'),
        ('finance', 'Finance & Banking'),
        ('education', 'Education & Training'),
        ('retail', 'Retail & E-commerce'),
        ('manufacturing', 'Manufacturing & Production'),
        ('other', 'Other')
    ]
    company_name = StringField('Company Name', validators=[
        DataRequired(message="Please enter your company name"),
        Length(min=2, max=100, message="Company name must be between 2 and 100 characters")
    ])
    company_email = EmailField('Email', validators=[
        DataRequired(message="Please enter your company email"),
        Email(message="Please enter a valid email address")
    ])
    company_phone = TelField('Phone Number', validators=[
        DataRequired(message="Please enter your company phone number"),
        Length(min=10, message="Please enter a valid phone number")
    ])
    company_location = StringField('Location', validators=[
        DataRequired(message="Please enter your company location"),
        Length(min=2, max=100, message="Location must be between 2 and 100 characters")
    ])
    company_industry = SelectField('Industry', 
        choices=INDUSTRY_CHOICES,
        validators=[DataRequired(message="Please select your company industry")]
    )
    submit = SubmitField('Make Save Changes')
    
class EditPassword(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter a password"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('company_password', message="Passwords must match")
    ])
    new_password =  PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('company_password', message="Passwords must match")
    ])
    
    
    