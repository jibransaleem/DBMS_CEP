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

    # Relationship to JobApplication
    job_applications = db.relationship('JobApplication', backref='candidate', lazy=True)


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
    # One-to-many relationship with JobApplication
    # job_applications = db.relationship('JobApplication', backref='company', lazy=True)


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
    job_skills= db.Column(db.String(150), nullable=False)
    job_type = db.Column(
        db.Enum("Trainee", "Internship", "Full-time", "Part-time"),
        nullable=False
    )
    job_dop = db.Column(db.String(30), nullable=False)  
    job_deadline = db.Column(db.Date, nullable=False)
    job_status = db.Column(db.Enum("open", "closed"), nullable=False, default="open")
    # One-to-many relationship with JobApplication
    job_applications = db.relationship('JobApplication', backref='jobposting', lazy=True)


# ---------------------- JobApplication Table ----------------------

class JobApplication(db.Model):
    __tablename__ = 'job_application'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resume_url = db.Column(db.String(300), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobposts.job_id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False) 
    apply_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)  # Set default to current time

# backref create reverse relation gbh job_appcaiton m nh krna pra

class SavedJob(db.Model):
    __tablename__ = 'saved_jobs'
    saved_job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobposts.job_id'), nullable=False)
    saved_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(500), nullable=True)  # Optional field for notes
    reminder_date = db.Column(db .Date, nullable=True)  # Optional reminder date for follow-up

    # Relationship to Candidate and JobPosting
    candidate = db.relationship('Candidate', backref=db.backref('saved_jobs', lazy=True))
    jobposting = db.relationship('JobPosting', backref=db.backref('saved_jobs', lazy=True))
