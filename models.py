from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Jibran123%40%23@localhost/DB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456789'

class Candidate(db.Model):
    __tablename__ = 'candidate'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)

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
