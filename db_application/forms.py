from flask_wtf import FlaskForm
from wtforms import StringField , EmailField , PasswordField , SubmitField
from wtforms.validators import Email , DataRequired  , length

class Register(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password" , validators= [DataRequired(), length(min=(6))])
    submit= SubmitField('Create Account')

class Login(FlaskForm):
    email = EmailField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password" , validators= [DataRequired(), length(min=(6))])
    Login= SubmitField('Login')