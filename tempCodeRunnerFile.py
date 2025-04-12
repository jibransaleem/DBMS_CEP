    form = RecruiterForm()
    data = Company.query.filter_by(company_id=session['user_id']).first()
    return render_template("edit_comp.html", form = form)