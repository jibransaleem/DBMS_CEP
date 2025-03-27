from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, SelectField
from wtforms.validators import Email, Length, DataRequired
from wtforms.fields import TelField

class RegisterUser(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone = TelField("Phone", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired(), Length(min=8)])
    option = SelectField("Role", choices=[("Company", "Company"), ("Employee", "Employee")])
    experience = StringField("Experience", validators=[DataRequired()])
    education = StringField("Education", validators=[DataRequired()])
    submit = SubmitField("Register")

# class LoginUser(FlaskForm):
#     email =  EmailField("email" , validators=[DataRequired(), Email()])
#     password =  StringField("passsword" , validators=[DataRequired(), length(min=6)])
#     option = SelectField('Login As', choices=[('Employee', 'Employee'), ('Company', 'Company')], validators=[DataRequired()])
#     submit = SubmitField("Login")