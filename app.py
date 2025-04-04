from flask import Flask, render_template, redirect, url_for, session, flash, request
from forms import JobSeekerForm, RecruiterForm, Login
from database import Config
from flask_mysqldb import MySQL
import bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = "123456789"

mysql = MySQL(app)

# ------------------ SIGNUP ROUTE ------------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    job_seeker_form = JobSeekerForm(prefix='job_seeker')
    recruiter_form = RecruiterForm(prefix='recruiter')

    if request.method == 'POST' and 'job_seeker-submit' in request.form and job_seeker_form.validate():
        name = job_seeker_form.name.data
        email = job_seeker_form.email.data
        phone = job_seeker_form.phone.data
        password = job_seeker_form.password.data
        confirm_password = job_seeker_form.confirm_password.data

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for("signup"))

        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT email FROM candidate WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('Email already taken by user!', 'error')
                return redirect(url_for("signup"))

            cursor.execute("INSERT INTO candidate (full_name, email, phone, pass) VALUES (%s, %s, %s, %s)", 
                           (name, email, phone, hash_password.decode("utf-8")))
            mysql.connection.commit()
            flash('Job seeker account created successfully!', 'success')
        except Exception as e:
            flash(f"An error occurred: {e}", 'error')
        finally:
            cursor.close()

        return redirect(url_for("login"))

    if request.method == 'POST' and 'recruiter-submit' in request.form and recruiter_form.validate():
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

        hashed_password = bcrypt.hashpw(company_password.encode("utf-8"), bcrypt.gensalt())

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT company_email FROM company WHERE company_email = %s", (company_email,))
            if cursor.fetchone():
                flash('Email already taken by user!', 'error')
                return redirect(url_for("signup"))

            cursor.execute("""
                INSERT INTO company (company_name, company_email, company_phone, company_location, company_industry, company_password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (company_name, company_email, company_phone, company_location, company_industry, hashed_password.decode("utf-8")))
            mysql.connection.commit()
            flash('Recruiter account created successfully!', 'success')
        except Exception as e:
            flash(f"An error occurred: {e}", 'error')
        finally:
            cursor.close()

        return redirect(url_for("login"))

    return render_template('signup.html', job_seeker_form=job_seeker_form, recruiter_form=recruiter_form)

# ------------------ LOGIN ROUTE ------------------

@app.route("/", methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        if session['Role'] == 'Candidate':
            return redirect(url_for("candidate"))
        elif session['Role'] == 'Company':
            return redirect(url_for("company"))

    form = Login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = form.Role.data

        try:
            cursor = mysql.connection.cursor()
            if role == "Candidate":
                cursor.execute("SELECT * FROM candidate WHERE email = %s", (email,))
            else:
                cursor.execute("SELECT * FROM company WHERE company_email = %s", (email,))
            data = cursor.fetchone()
        except Exception as e:
            flash(f"An error occurred: {e}", 'error')
            return redirect(url_for("login"))
        finally:
            cursor.close()

        if not data:
            flash("Incorrect Email!", "warning")
            return redirect(url_for("login"))

        stored_email = data[2]
        if stored_email != email:
            flash("Incorrect Email!", "warning")
            return redirect(url_for("login"))

        if not bcrypt.checkpw(password.encode("utf-8"), data[-1].encode("utf-8")):
            flash("Incorrect Password!", "warning")
            return redirect(url_for("login"))

        session['user_id'] = data[0]
        session['Role'] = role

        if role == "Candidate":
            return redirect(url_for("candidate"))
        return redirect(url_for("company"))

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

# ------------------ RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True)
