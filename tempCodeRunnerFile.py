class JobApplication(db.Model):
    __tablename__ = 'job_application'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resume_url = db.Column(db.String(300), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobposts.job_id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False) 
    apply_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)  # Set default to current time
    