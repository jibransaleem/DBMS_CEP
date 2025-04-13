from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Jibran123%40%23@localhost/DB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456789'

# ---------------------- Candidate Table ----------------------

class Candidate(db.Model):
    __tablename__ = 'candidate'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# ---------------------- Company Table ----------------------

class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_email = db.Column(db.String(255), nullable=False, unique=True)
    company_phone = db.Column(db.String(15), nullable=False)
    company_location = db.Column(db.String(100), nullable=False)
    company_industry = db.Column(
        db.Enum('technology', 'healthcare', 'finance', 'education', 'retail', 'manufacturing', 'other'),
        nullable=False
    )
    company_password = db.Column(db.String(255), nullable=False)
    
    # One-to-many relationship with JobPosting
    job_posts = db.relationship('JobPosting', backref='company', cascade="all, delete", lazy=True)

# ---------------------- JobPosting Table ----------------------

class JobPosting(db.Model):
    __tablename__ = 'jobposts'

    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(300), nullable=False)
    job_qualification = db.Column(db.String(300), nullable=False)
    job_location = db.Column(db.String(100), nullable=False)
    job_city = db.Column(db.String(20), nullable=False)
    job_industry = db.Column(
        db.Enum('technology', 'healthcare', 'finance', 'education', 'retail', 'manufacturing', 'other'),
        nullable=False
    )
    job_salary = db.Column(
        db.Enum('Below 30,000', '30,000 - 50,000', '50,000 - 70,000', '70,000 - 100,000', 'Above 100,000'),
        nullable=False
    )
    job_skills= db.Column(db.String(150) , nullable = False)
    job_type = db.Column(
        db.Enum("Trainee", "Internship", "Full-time", "Part-time"),
        nullable=False
    )
    job_dop = db.Column(db.String(30 ),  nullable = False)  
    job_deadline = db.Column(db.Date, nullable=False)
    job_status = db.Column(db.Enum("open", "closed"), nullable=False, default="open")

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)