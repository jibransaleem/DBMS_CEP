from flask import Flask, render_template, redirect, flash, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Jibran123%40%23@localhost/Prac'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456789'

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)

# User Registration Form
class UserForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

# Register
@app.route("/", methods=["GET", "POST"])
def sign():
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already exists", "danger")
            return redirect(url_for('sign'))

        hashed_password = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt())
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password.decode("utf-8"))
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template("Reg.html", form=form)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode("utf-8"), user.password.encode("utf-8")):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('page'))
        else:
            flash("Invalid credentials", "danger")
    return render_template("home.html", form=form)

# Dashboard Page
@app.route("/page")
def page():
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('login'))
    return render_template("page.html", user_name=session.get('user_name'))

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
