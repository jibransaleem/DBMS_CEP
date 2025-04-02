from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

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

