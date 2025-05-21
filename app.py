from flask import Flask, render_template, redirect, url_for, session, flash, request
from forms import JobSeekerForm, RecruiterForm, Login, JobPostForm, JobApplicationForm,EditPassword, Edit_Company,SavedJobForm
import bcrypt
from models import db, Config, Candidate, Company, JobPosting, JobApplication, SavedJob 
from datetime import datetime
from sqlalchemy import func  , desc

import os
import secrets
import time
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from helper import is_strong_password, is_valid_name,is_valid_company,validate_contact_number


app = Flask(__name__, template_folder='templates', static_folder="static", static_url_path="/")
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)
#saad
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    job_seeker_form = JobSeekerForm(prefix='job_seeker')
    recruiter_form = RecruiterForm(prefix='recruiter')

    if request.method == 'POST':
        # -------- Job Seeker Signup --------
        if 'job_seeker-submit' in request.form and job_seeker_form.validate():
            name = job_seeker_form.name.data
            email = job_seeker_form.email.data
            phone = job_seeker_form.phone.data
            password = job_seeker_form.password.data
            confirm_password = job_seeker_form.confirm_password.data
            if not  is_valid_name(name):
                flash('Kindly Enter Correct name ', 'error')
                return redirect(url_for("signup"))
            if not validate_contact_number(phone) :
                flash('Kindly Enter Correct contact Number.', 'error')
                return redirect(url_for("signup"))
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return redirect(url_for("signup"))
            if not is_strong_password(password) :    
                flash('Please Enter Strong Password', 'error')
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            try:
                if Candidate.query.filter_by(email=email).first():
                    flash('Email already taken by another user!', 'error')
                    return redirect(url_for("signup"))

                user = Candidate(full_name=name, email=email, phone=phone, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash('Job seeker account created successfully!', 'success')
                return redirect(url_for("login"))
            except Exception as e:
                flash(f"An error occurred: {e}", 'error')

        # -------- Recruiter Signup --------
        if 'recruiter-submit' in request.form and recruiter_form.validate():
            company_name = recruiter_form.company_name.data
            company_email = recruiter_form.company_email.data
            company_phone = recruiter_form.company_phone.data
            company_location = recruiter_form.company_location.data
            company_industry = recruiter_form.company_industry.data
            company_password = recruiter_form.company_password.data
            company_re_password = recruiter_form.company_confirm_password.data
            if not  is_valid_company(company_name):
                flash('Kindly Enter Correct Company  name ', 'error')
                return redirect(url_for("signup"))
            if not validate_contact_number(company_phone) :
                flash('Kindly Enter Correct contact Number.', 'error')
                return redirect(url_for("signup"))
            elif company_password != company_re_password:
                flash("Passwords do not match!", "error")
                return redirect(url_for("signup"))
            elif not is_strong_password(company_password) :
                    flash('Please Enter Strong Password', 'error')
                    return redirect(url_for("signup"))
                    
            hashed_password = bcrypt.hashpw(company_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            try:
                if Company.query.filter_by(company_email=company_email).first():
                    flash('Email already taken by another user!', 'error')
                    return redirect(url_for("signup"))

                user = Company(
                    company_name=company_name,
                    company_email=company_email,
                    company_phone=company_phone,
                    company_location=company_location,
                    company_industry=company_industry,
                    company_password=hashed_password
                )
                db.session.add(user)
                db.session.commit()
                flash('Recruiter account created successfully!', 'success')
                return redirect(url_for("login"))
            except Exception as e:
                flash(f"An error occurred: {e}", 'error')

    return render_template('signup.html', job_seeker_form=job_seeker_form, recruiter_form=recruiter_form)

# ------------------ LOGIN ROUTE ------------------
#saad
@app.route("/", methods=['GET', 'POST'])
def login():
    if "user_id" in session and 'Role' in session:
        return redirect(url_for("candidate" if session['Role'] == 'Candidate' else "company"))
    form = Login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = form.Role.data
        if role == 'Company':
            user = Company.query.filter_by(company_email=email).first()
            key = user.company_password if user else None
        else:
            user = Candidate.query.filter_by(email=email).first()
            key = user.password if user else None
        if user is None or not bcrypt.checkpw(password.encode("utf-8"), key.encode("utf-8")):
            flash("Invalid email or password!", "danger")
            return redirect(url_for("login"))
        session['user_id'] = user.id
        session['Role'] = role
        if role == "Candidate" :
            return redirect(url_for("candidate"))

    return render_template("login.html", form=form)

# ------------------ LOGOUT ------------------
#saad
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("Role", None)
    return redirect(url_for('login'))

# ------------------ PROTECTED DASHBOARDS ------------------
# db.session is your active database sessiosion(connection)
@app.route("/candidate")
def candidate():
    if "user_id" not in session or session.get("Role") != "Candidate":
        flash("Please login as a Candidate to continue", "warning")
        return redirect(url_for("login"))
    candidate = db.session.query(Candidate).filter(Candidate.id == session['user_id']).first()
    return render_template("cand.html", name = candidate.full_name)
def get_latest_job_posting():   
    latest_job = (
    db.session.query(JobPosting)
    .filter(JobPosting.company_id == session["userid"])
    .order_by(JobPosting.job_id.desc())
    .first()
)
    db.session.query(JobPosting)
    if latest_job is None:
        return None
    return {
        "job_id": latest_job.job_id,
        "job_title": latest_job.job_title,  # Ensure job_title is included
        "job_status": latest_job.job_status,
        "job_dop": latest_job.job_dop,
        "job_skills": latest_job.job_skills,
        "job_location" : latest_job.job_location,
        "job_salary" : latest_job.job_salary,
        "job_industry":latest_job.job_industry
    }
    
# taha
@app.route("/company")
def company():
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    data = Company.query.filter_by(id=session["user_id"]).first()
    featured_job = JobPosting.query\
    .filter_by(company_id=session['user_id'])\
    .order_by(desc(JobPosting.job_dop))\
    .first()
    if featured_job is not None:
        return render_template("company.html",company_name =data.company_name , featured_jobs = featured_job)
    return render_template("company.html",company_name =data.company_name)

#taha
@app.route("/CompanyDetails" , methods  = ['GET'])
def CompanyDetails():
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    Company_Details = Company.query.filter_by(id = session['user_id']).first()
    return render_template("Company_details.html" , data = Company_Details)
@app.route("/EditCompanyDetails", methods=['POST', 'GET'])
def Edit_Company_Details():
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    form = Edit_Company()
    data = Company.query.filter_by(id=session['user_id']).first()
    if request.method == "POST" and form.validate_on_submit():
        data.company_name = form.company_name.data
        data.company_email = form.company_email.data
        data.company_phone = form.company_phone.data
        data.company_location = form.company_location.data
        data.company_industry = form.company_industry.data
        db.session.commit()
        flash('Company details updated successfully!', 'success')
    elif request.method == "GET":
        form.company_name.data = data.company_name
        form.company_email.data = data.company_email
        form.company_phone.data = data.company_phone
        form.company_location.data = data.company_location
        form.company_industry.data = data.company_industry

    return render_template("edit_comp.html", form=form, data=data)
#taha
@app.route("/view_Jobs")
def Jobs_for_edit():
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    job = JobPosting.query.filter_by(company_id = session['user_id']).all()
    return render_template("edit_job.html", jobs=job)

# COMPANY KR RH H JOB EDIT
@app.route("/job/edit/<int:job_id>", methods=['GET', 'POST'])
def Edit_Jobs(job_id):
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    editJob = JobPostForm()
    job = JobPosting.query.get_or_404(job_id)
    if editJob.validate_on_submit():
        job.job_title = editJob.title.data
        job.job_description = editJob.description.data
        job.job_qualification = editJob.qualification.data
        job.job_location = editJob.location.data
        job.job_city = editJob.city.data
        job.job_type = editJob.job_type.data
        job.job_salary = editJob.salary.data
        job.job_skills = editJob.skills.data
        job.job_industry = editJob.job_industry.data
        job.job_status = editJob.job_status.data
        job.job_deadline = editJob.dead_line.data

        db.session.commit()
        flash('Job updated successfully!', 'success')

    elif request.method == 'GET':
        editJob.title.data = job.job_title  # Corrected from job.titlle
        editJob.description.data = job.job_description
        editJob.qualification.data = job.job_qualification
        editJob.location.data = job.job_location
        editJob.city.data = job.job_city
        editJob.job_type.data = job.job_type
        editJob.salary.data = job.job_salary
        editJob.skills.data = job.job_skills
        editJob.job_industry.data = job.job_industry
        editJob.job_status.data = job.job_status
        editJob.dead_line.data = job.job_deadline

    return render_template("Edit_company_jobs.html", form=editJob, job=job)

#COMAPNY KREGI JOB POST
#aans
@app.route("/PostJob", methods=['POST', 'GET'])
def Post_Jobs():
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    form = JobPostForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        qualification = form.qualification.data
        location = form.location.data
        city = form.city.data
        status = form.job_status.data
        deadline = form.dead_line.data
        salary = form.salary.data
        skills = form.skills.data
        job_type = form.job_type.data
        current_time = datetime.now()
        dop = current_time.strftime("%Y-%m-%d")
        job_industry = form.job_industry.data
        job_data = JobPosting(
            job_deadline=deadline,
            job_status=status,
            job_title=title,
            job_industry=job_industry,
            job_description=description,
            job_qualification=qualification,
            job_location=location,
            job_city=city,
            job_skills=skills,
            job_salary=salary,
            job_type=job_type,
            job_dop=dop,
            company_id=session['user_id']
        )
        db.session.add(job_data)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('Post_Jobs'))
    return render_template("post_job.html", form=form)

# COMPANY K SARO JOBS Y HEN
#aanas
@app.route("/ViewJob")
def View_Jobs():
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    job = JobPosting.query.filter_by(company_id=session['user_id']).all()
    
    return render_template("view_jobs.html", jobs=job)


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    # Initialize query
    query = JobPosting.query

    # Get filter parameters from form (POST) or query string (GET)
    job_type = request.form.get("jobTypeFilter") or request.args.get("jobTypeFilter")
    city = request.form.get("locationFilter") or request.args.get("locationFilter")
    industry = request.form.get("industryFilter") or request.args.get("industryFilter")
    salary_range = request.form.get("experienceFilter") or request.args.get("experienceFilter")

    # Apply filters if provided
    if job_type:
        query = query.filter(JobPosting.job_type.ilike(f"%{job_type}%"))
    if city:
        query = query.filter(JobPosting.job_city.ilike(f"%{city}%"))
    if industry:
        query = query.filter(JobPosting.job_industry.ilike(f"%{industry}%"))
    if salary_range:
        # Assuming job_salary is stored as a string like "$50,000 - $70,000" or a numeric value
        # Adjust this logic based on your database schema
        if salary_range == "below-30k":
            query = query.filter(JobPosting.job_salary.ilike("%below 30,000%"))
        elif salary_range == "30k-50k":
            query = query.filter(JobPosting.job_salary.ilike("%30,000 - 50,000%"))
        elif salary_range == "50k-70k":
            query = query.filter(JobPosting.job_salary.ilike("%50,000 - 70,000%"))
        elif salary_range == "70k-100k":
            query = query.filter(JobPosting.job_salary.ilike("%70,000 - 100,000%"))
        elif salary_range == "above-100k":
            query = query.filter(JobPosting.job_salary.ilike("%above 100,000%"))

    # Execute query to get filtered jobs
    jobs = query.all()

    # Get unique city names for the City filter dropdown
    unique_cities = db.session.query(JobPosting.job_city).distinct().all()
    city_names = [city[0] for city in unique_cities if city[0]]

    return render_template("jobs.html", jobs=jobs, city_names=city_names)

@app.route("/applyjob/<int:job_id>", methods=['GET', 'POST'])
#jibran
def apply_job(job_id):
    form = JobApplicationForm()
    job = JobPosting.query.filter_by(job_id=job_id).first()
    if not job:
        flash('Job not found!', 'error')
        return redirect(url_for('jobs'))
    if form.validate_on_submit():
        candidate_id = session['user_id']
        existing_application = JobApplication.query.filter_by(job_id=job_id, candidate_id=candidate_id).first()
        if existing_application:
            flash('You have already applied for this job!', 'warning')
            return redirect(url_for("apply_job", job_id=job_id))
        file = form.resume.data
        file_name = secure_filename(file.filename)
        upload_folder = os.path.join(app.root_path, 'static', 'resumes')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file_name)
        file.save(file_path)
        url = url_for('static', filename=f'resumes/{file_name}', _external=True)
        apply_date = datetime.utcnow().date()
        data = JobApplication(
            resume_url=url,
            job_id=job_id,
            candidate_id=candidate_id,
            apply_date=apply_date
        )
        db.session.add(data)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for("apply_job", job_id=job_id))
    return render_template("apply.html", job=job, form=form)
# USER N KHN KHN AOPPLY KIA
#jibran 
@app.route("/Myapplications")
def My_applications():
    applied_jobs = db.session.query(JobPosting, JobApplication, Company).\
        join(JobApplication, JobPosting.job_id == JobApplication.job_id).\
        join(Company, JobPosting.company_id == Company.id).\
        filter(JobApplication.candidate_id == session['user_id']).\
        all()
    return render_template('myjobs.html', data=applied_jobs)

# company KO JO JOBS RECIVED HOI
#anas
@app.route('/recivedjobs')
def recivedjobs():
    job_type = request.args.get('job_type', '').strip()
    industry = request.args.get('industry', '').strip()
    apply_date = request.args.get('apply_date', '').strip()
    filter_flags = {
        'job_type_applied': bool(job_type),
        'industry_applied': bool(industry),
        'apply_date_applied': bool(apply_date)
    }
    filters_applied = any(filter_flags.values())
    query = db.session.query(
        Candidate.full_name , 
        JobPosting.job_title , 
        JobPosting.job_type , 
        JobApplication.apply_date,
        JobApplication.resume_url,
        JobPosting.job_industry
    ).join(
        JobPosting, JobApplication.job_id == JobPosting.job_id
    ).join(
        Candidate, JobApplication.candidate_id == Candidate.id
    ).filter(
        JobPosting.company_id == session['user_id']
    )
    if job_type:
        query = query.filter(JobPosting.job_type == job_type)
    if industry:
        query = query.filter(JobPosting.job_industry == industry)
    if apply_date:
        query = query.filter(JobApplication.apply_date == apply_date)
    applications = query.all()
    return render_template(
        'recieved_jobs.html',
        data=applications,
        filters_applied=filters_applied
    )
#jibran
@app.route("/see_application/<int:job_id>", methods=['GET', 'POST'])
def see_my_application(job_id):
    result = (
    db.session.query(JobPosting, JobApplication)
    .join(JobApplication, JobApplication.job_id == JobPosting.job_id)
    .filter(
        JobApplication.candidate_id == session["user_id"],
        JobPosting.job_id == job_id
    )
    .first()
    )

    if result:
        job_posting, job_application = result
        combined_data = {
        # JobPosting fields
        "job_id": job_posting.job_id,
        "job_title": job_posting.job_title,
        "job_description": job_posting.job_description,
        "job_qualification": job_posting.job_qualification,
        "job_location": job_posting.job_location,
        "job_city": job_posting.job_city,
        "job_industry": job_posting.job_industry,
        "job_salary": job_posting.job_salary,
        "job_skills": job_posting.job_skills,
        "job_type": job_posting.job_type,
        "job_dop": job_posting.job_dop,
        "job_deadline": job_posting.job_deadline,
        "job_status": job_posting.job_status,

        # JobApplication fields
        "application_id": job_application.id,
        "candidate_id": job_application.candidate_id,
        "apply_date": job_application.apply_date,
    }
    company_id =  job_posting.company_id
    name = db.session.query(Company.company_name).filter(Company.id == company_id).first()
    return render_template('view_appli.html', Application_data=combined_data,company_name = name  )

# ------------------ SAVED JOBS ROUTES ------------------


@app.route("/save_job/<int:job_id>", methods=['GET', 'POST'])
def save_job(job_id):
    if 'user_id' not in session or session.get('Role') != 'Candidate':
        flash('Please login as a Candidate to save jobs', 'warning')
        return redirect(url_for('login'))

    form = SavedJobForm()
    job = JobPosting.query.filter_by(job_id=job_id).first()

    if not job:
        flash('Job not found!', 'error')
        return redirect(url_for('jobs'))

    company = Company.query.filter_by(id=job.company_id).first()

    data_to_send = {
        "job_title": job.job_title,
        "job_id": job.job_id,
        "job_city": job.job_city,
        "job_salary": job.job_salary,
        "job_skills": job.job_skills,
        "job_deadline": job.job_deadline,
        "company_name": company.company_name
    }

    if request.method == "POST":
        # Check if the job is already saved
        existing_saved_job = SavedJob.query.filter_by(job_id=job_id, candidate_id=session['user_id']).first()
        if existing_saved_job:
            flash('This job is already saved!', 'warning')
            return redirect(url_for('jobs'))

        if form.validate_on_submit():
            notes = form.notes.data
            reminder_date = form.reminder_date.data
            saved_job = SavedJob(
                candidate_id=session['user_id'],
                job_id=job_id,
                notes=notes,
                reminder_date=reminder_date
            )
            db.session.add(saved_job)
            db.session.commit()
            flash('Job saved successfully!', 'success')
            # Use PRG pattern to avoid form resubmission on back
            

    return render_template("saved_job.html", form=form, data=data_to_send)


@app.route("/saved_jobs")
def My_save_jobs():
    if 'user_id' not in session or session.get('Role') != 'Candidate':
        flash('Please login as a Candidate to view saved jobs', 'warning')
        return redirect(url_for('login'))

    saved_jobs = (
        db.session.query(
        SavedJob.saved_at,
        SavedJob.notes,
        JobPosting.job_title,
        JobPosting.job_location,
        JobPosting.job_city,
        JobPosting.job_salary,
        Company.company_name.label('company_name')
    )
    .join(JobPosting, JobPosting.job_id == SavedJob.job_id)
    .join(Company, Company.id == JobPosting.company_id)
    .filter(SavedJob.candidate_id == session["user_id"])
    .all()
    )

    return render_template('my_saved_jobs.html', data=saved_jobs)
if __name__ == '__main__':
    app.run(debug=True)
    