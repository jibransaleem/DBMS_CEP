from flask import Flask, render_template, redirect, url_for, session, flash, request
from forms import JobSeekerForm, RecruiterForm, Login, JobPostForm, JobApplicationForm,EditPassword, Edit_Company
import bcrypt
from models import db, Config, Candidate, Company, JobPosting, JobApplication, SavedJob 
from datetime import datetime
from sqlalchemy import func
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from helper import is_strong_password, is_valid_name,is_valid_company,validate_contact_number

app = Flask(__name__, template_folder='templates', static_folder="static", static_url_path="/")
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

# ------------------ SIGNUP ROUTE ------------------

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

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("Role", None)
    return redirect(url_for('login'))

# ------------------ PROTECTED DASHBOARDS ------------------

@app.route("/candidate")
def candidate():
    if "user_id" not in session or session.get("Role") != "Candidate":
        flash("Please login as a Candidate to continue", "warning")
        return redirect(url_for("login"))
    return render_template("cand.html")
def get_latest_job_posting():
    latest_job = db.session.query(JobPosting).order_by(JobPosting.job_id.desc()).first()
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
@app.route("/company")
def company():
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    data = Company.query.filter_by(id=session["user_id"]).first()
    featured_jobs = get_latest_job_posting()
    if featured_jobs is not None:
        return render_template("company.html",company_name =data.company_name , featured_jobs = featured_jobs)
    return render_template("company.html",company_name =data.company_name)


@app.route("/EditCompanyDetails", methods=['POST', 'GET'])
def Edit_Company_Details():
    form = Edit_Company()
    if 'user_id' not in session:
        flash('User not logged in!', 'error')
        return redirect(url_for('login'))
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

@app.route("/view_Jobs")
def Jobs_for_edit():
    job = JobPosting.query.filter_by(company_id = session['user_id']).all()
    return render_template("edit_job.html", jobs=job)

@app.route("/job/edit/<int:job_id>", methods=['GET', 'POST'])
def Edit_Jobs(job_id):
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
@app.route("/PostJob", methods=['POST', 'GET'])
def Post_Jobs():
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

@app.route("/ViewJob")
def View_Jobs():
    job = JobPosting.query.filter_by(company_id=session['user_id']).all()
    return render_template("view_jobs.html", jobs=job)

@app.route("/jobs")
def Jobs():
    job = JobPosting.query.all()
    return render_template("jobs.html", jobs=job)
# isme glti arhi h 
@app.route("/applyjob/<int:job_id>", methods=['GET', 'POST'])
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

@app.route("/Myapplications")
def My_applications():
    applied_jobs = db.session.query(JobPosting, JobApplication, Company).\
        join(JobApplication, JobPosting.job_id == JobApplication.job_id).\
        join(Company, JobPosting.company_id == Company.id).\
        filter(JobApplication.candidate_id == session['user_id']).\
        all()
    return render_template('myjobs.html', data=applied_jobs)

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
        Candidate.full_name.label("full_name"),
        JobPosting.job_title.label("job_title"),
        JobPosting.job_type.label("job_type"),
        JobApplication.apply_date.label("apply_date"),
        JobApplication.resume_url.label("resume_url"),
        JobPosting.job_industry.label("job_industry")
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

# ------------------ SAVED JOBS ROUTES ------------------

@app.route("/save_job/<int:job_id>", methods=['POST'])
def save_job(job_id):
    if 'user_id' not in session or session.get('Role') != 'Candidate':
        flash('Please login as a Candidate to save jobs', 'warning')
        return redirect(url_for('login'))
    job = JobPosting.query.filter_by(job_id=job_id).first()
    if not job:
        flash('Job not found!', 'error')
        return redirect(url_for('jobs'))
    existing_saved_job = SavedJob.query.filter_by(job_id=job_id, candidate_id=session['user_id']).first()
    if existing_saved_job:
        flash('This job is already saved!', 'warning')
        return redirect(url_for('jobs'))
    notes = request.form.get('notes', None)
    reminder_date = request.form.get('reminder_date', None)
    if reminder_date:
        try:
            reminder_date = datetime.strptime(reminder_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid reminder date format!', 'error')
            return redirect(url_for('jobs'))
    saved_job = SavedJob(
        candidate_id=session['user_id'],
        job_id=job_id,
        notes=notes,
        reminder_date=reminder_date
    )
    db.session.add(saved_job)
    db.session.commit()
    flash('Job saved successfully!', 'success')
    return redirect(url_for('jobs'))

@app.route("/saved_jobs")
def saved_jobs():
    if 'user_id' not in session or session.get('Role') != 'Candidate':
        flash('Please login as a Candidate to view saved jobs', 'warning')
        return redirect(url_for('login'))
    saved_jobs = db.session.query(SavedJob, JobPosting, Company).\
        join(JobPosting, SavedJob.job_id == JobPosting.job_id).\
        join(Company, JobPosting.company_id == Company.id).\
        filter(SavedJob.candidate_id == session['user_id']).\
        all()
    return render_template('saved_jobs.html', data=saved_jobs)
@app.route("/ChangePassword", methods=['GET', 'POST'])
def Change_password():
    if "user_id" not in session.keys():
        return redirect(url_for("login"))

    EditForm = EditPassword()
    role = session['Role']

    if request.method == "POST":
        if EditForm.validate_on_submit():
            old_pass = EditForm.password.data
            confirm_pass = EditForm.confirm_password.data
            new_password = EditForm.new_password.data

            if new_password != confirm_pass:
                flash("Passwords do not match", "error")
                return render_template("change_Password.html", EditForm=EditForm)

            if role.lower() == "company":
                user = Company.query.get_or_404(session["user_id"])
                user_pass_ = user.company_password
            else:
                user = Candidate.query.get_or_404(session["user_id"])
                user_pass_ = user.password

            if not bcrypt.checkpw(old_pass.encode("utf-8"), user_pass_.encode("utf-8")):
                flash("Incorrect old password", "error")
                return render_template("change_Password.html", EditForm=EditForm)

            if not is_strong_password(new_password):
                flash("Please choose a stronger password", "error")
                return render_template("change_Password.html", EditForm=EditForm)

            hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            if role.lower() == "company":
                user.company_password = hashed_password
            else:
                user.password = hashed_password

            db.session.commit()
            flash('Password updated successfully!', 'success')
            return render_template("change_Password.html", EditForm=EditForm)

    return render_template("change_Password.html", EditForm=EditForm)
            
    # ------------------ RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True)