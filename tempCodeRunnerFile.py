@app.route("/PostJob" , methods =['POST', 'GET'])
def Post_Jobs() :
    form = JobPostForm()
    if form.validate_on_submit() :
        title =  form.title.data 
        description = form.description.data
        qualification = form.qualification.data
        location = form.location.data
        city = form.city.data
        salary = form.salary.data
        skills =  form.skills.data
        job_type = form.job_type.data
        current_time = datetime.now()
        dop = current_time.strftime("%d-%m-%Y")
        job_industry = form.job_industry.data
        job_data = JobPosting(
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
        return redirect(url_for('post_job'))
# Add the new job posting to the session and commit it to the database
    return render_template("post_job.html", form = form)