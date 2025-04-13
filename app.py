from flask import Flask, render_template, redirect, url_for, session, flash, request
from forms import JobSeekerForm, RecruiterForm, Login , JobPostForm
import bcrypt
from models import db, Config, Candidate, Company ,JobPosting
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

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

            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return redirect(url_for("signup"))

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

            if company_password != company_re_password:
                flash("Passwords do not match!", "error")
                return redirect(url_for("signup"))

            hashed_password = bcrypt.hashpw(company_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            try:
                if  Company.query.filter_by(company_email=company_email).first():
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
    if "user_id" and 'Role' in session:
        return redirect(url_for("candidate" if session['Role'] == 'Candidate' else "company"))
    form = Login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = form.Role.data

        if role == 'Company':
            user = Company.query.filter_by(company_email=email).first()
            key = user.company_password
        else:
            user = Candidate.query.filter_by(email=email).first()
            key = user.password
        if user is None or key is None:
            flash("User not found!", "danger")
            return redirect(url_for("login"))

        
        if not bcrypt.checkpw(password.encode("utf-8"), key.encode("utf-8")):
            flash("Incorrect Password!", "warning")
            return redirect(url_for("login"))

        session['user_id'] = user.id
        session['Role'] = role
        return redirect(url_for("candidate" if role == "Candidate" else "company"))

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

@app.route("/company")
def company():
    if "user_id" not in session or session.get("Role") != "Company":
        flash("Please login as a Company to continue", "warning")
        return redirect(url_for("login"))
    return render_template("company.html")

@app.route("/ChangePassword")
def Edit_password() :
    return render_template("change_password.html")
@app.route("/EditCompanyDetails", methods=['GET', 'POST'])
def Edit_Company_Details():
    form = RecruiterForm()
    data = Company.query.filter_by(id=session['user_id']).first()

    if 'user_id' not in session:
        flash('User not logged in!', 'error')
        return redirect(url_for('login'))
    if request.method == "POST" and form.validate_on_submit():
        # Process form data
        data.company_name = form.company_name.data
        data.company_email = form.company_email.data
        data.company_phone = form.company_phone.data
        data.company_location = form.company_location.data
        data.company_industry = form.company_industry.data

        db.session.commit()
        flash('Company details updated successfully!', 'success')
        return redirect(url_for('company'))  # Adjust this to where you want to go after submission

    return render_template("edit_comp.html", form=form, data=data)
@app.route("/EditJobs")
def Edit_Jobs() :
    return render_template("edit_job.html")
@app.route("/PostJob" , methods =['POST', 'GET'])
def Post_Jobs() :
    form = JobPostForm()
    if form.validate_on_submit() :
        title =  form.title.data 
        description = form.description.data
        qualification = form.qualification.data
        location = form.location.data
        city = form.city.data
        status = form.job_status.data
        deadline =  form.dead_line.data
        salary = form.salary.data
        skills =  form.skills.data
        job_type = form.job_type.data
        current_time = datetime.now()
        dop = current_time.strftime("%Y-%m-%d")
        job_industry = form.job_industry.data
        job_data = JobPosting(
            job_deadline = deadline ,
            job_status = status ,
            job_title=title,
            job_industry =  job_industry , 
            job_description=description,
            job_qualification=qualification,
            job_location=location,
            job_city=city,
            job_skills = skills,
            job_salary=salary,  
            job_type=job_type,  
            job_dop=dop,       
            company_id=session['user_id']  # Make sure this is fetched correctly
)
        db.session.add(job_data)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('Post_Jobs'))
# Add the new job posting to the session and commit it to the database
    return render_template("post_job.html", form = form)
@app.route("/ViewApplications")
def View_Applications() :
    return "<h1>GOOD</h1>"
    
@app.route("/ViewJob")
def View_Jobs():
    job = JobPosting.query.filter_by(company_id=session['user_id']).all()
    return render_template("view_jobs.html", jobs=job)



@app.route("/jobs")
def Jobs():
    job = JobPosting.query.all()
    return render_template("jobs.html", jobs=job)
    
# ------------------ RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True)
