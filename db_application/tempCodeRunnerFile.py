@app.route('/', methods = ['GET','POST'])
def login():
    form = Login() 
    Flag = True
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data 
            # opening data base
            if email and email and password  :
                cursor = mysql.connection.cursor() 
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                result = cursor.fetchone()  
                Flag = False
                if  result :
                    if bcrypt.checkpw(password.encode("utf-8"), result[3].encode("utf-8"))  :
                        cursor.close()
                        flash("Login" ,'Success')   
                        return redirect('/home')
                else:
                    cursor.close()
                    if Flag == False:
                        flash("In correct Email ! " ,"danger")
                    else:
                        flash("In correct Pasword ! ", "danger")
                    return render_template("login.html", form = form)
    return render_template("login.html", form = form)



