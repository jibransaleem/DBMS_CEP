from forms import JobSeekerForm, RecruiterForm
from flask import Flask , render_template , redirect , url_for , session , flash , request
from database import Config
import os
from flask_mysqldb  import MySQL
import bcrypt
app = Flask(__name__)

app.config.from_object(Config)
app.config['SECRET_KEY'] =os.urandom(24)   # Replace with a real secret key in production

mysql = MySQL(app)
@app.route('/')
def home():
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    job_seeker_form = JobSeekerForm(prefix='job_seeker')
    recruiter_form = RecruiterForm(prefix='recruiter')
    
    # Check if job seeker form was submitted
    if job_seeker_form.submit.data and job_seeker_form.validate_on_submit() :
        # Process job seeker form
        name = job_seeker_form.name.data
        email = job_seeker_form.email.data
        phone = job_seeker_form.phone.data
        password = job_seeker_form.password.data
        confirm_password = job_seeker_form.confirm_password.data
        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        if name and email and phone and password and confirm_password and(password == confirm_password ): 
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO candidate (full_name, email, phone, pass) VALUES (%s, %s, %s, %s)", 
            (name, email, phone, hash_password))  
            mysql.connection.commit()  # Commit changes
            cursor.close()  # Close cursor
        # Here you would typically hash the password and save to database
        # hashed_password = generate_password_hash(password)
        # db.add_job_seeker(name, email,hone, hashed_password)
        
            flash('Job seeker account created successfully!', 'success')
            return redirect(url_for('login'))
            
    
    # Check if recruiter form was submitted
    if recruiter_form.submit.data and recruiter_form.validate_on_submit():
        # Process recruiter form
        company_name = recruiter_form.company_name.data
        company_email = recruiter_form.company_email.data
        company_phone = recruiter_form.company_phone.data
        company_location = recruiter_form.company_location.data
        company_industry = recruiter_form.company_industry.data
        company_password = recruiter_form.company_password.data
        company_re_password = recruiter_form.company_confirm_password.data
        hashed_password = bcrypt.hashpw(company_password.encode("utf-8"), bcrypt.gensalt())
        if company_name and company_email and company_location and company_industry and( company_re_password==company_password)  :
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO company (company_name, company_email, company_phone, company_location, company_industry, company_password) VALUES (%s, %s, %s, %s, %s, %s)", 
                (company_name, company_email, company_phone, company_location, company_industry, hashed_password))  
            mysql.connection.commit()  # Commit changes
            cursor.close()  
        # Here you would typically hash the password and save to database
        # hashed_password = generate_password_hash(company_password)
        # db.add_recruiter(company_name, company_email, company_phone, company_location, company_industry, hashed_password)
        
        flash('Recruiter account created successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', 
                          job_seeker_form=job_seeker_form, 
                          recruiter_form=recruiter_form)

@app.route('/login')
def login():
    # This would be your login page
    return render_template('login.html')  # You would need to create this template

if __name__ == '__main__':
    app.run(debug=True)

