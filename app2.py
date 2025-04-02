# from flask import Flask , render_template , redirect , url_for , session , flash , request
# from database import Config
# import os
# from flask_mysqldb  import MySQL
# from forms import Register , Login
# import bcrypt
# app =  Flask(__name__ , template_folder='templates')
# app.config.from_object(Config)
# app.secret_key = os.urandom(20) 
# mysql = MySQL(app)
# @app.route('/')
# def home():
#     if "user_id" not in session.keys():
#         return redirect("/login")
#     return render_template("home.html")
# @app.route('/signup' , methods = ["GET","POST"])
# def signup():
#     form = Register() 
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             name = form.name.data
#             email = form.email.data
#             password = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt())
#             # opening data base
#             if name and email and password  :
#                 cursor = mysql.connection.cursor() 
#                 cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#                 result = cursor.fetchone()  
#                 if not result :
#                     cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
#                     cursor.connection.commit()
#                     cursor.close()
#                     flash("Account has created" ,'success')   
#                     return redirect('/')
#                 else:
#                     flash("Account already exist ! Try different email" ,"danger")
#                     return render_template("signup.html", form = form)
#     return render_template("signup.html", form = form)
# @app.route('/login', methods = ['GET','POST'])
# def login():
#     form = Login() 
#     Flag = True
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             email = form.email.data
#             password = form.password.data 
#             # opening data base
#             if email and email and password  :
#                 cursor = mysql.connection.cursor() 
#                 cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#                 result = cursor.fetchone()  
#                 Flag = False
#                 if  result :
#                     session["user_id"] = result[0]
#                     if bcrypt.checkpw(password.encode("utf-8"), result[3].encode("utf-8"))  :
#                         cursor.close()
#                         flash("Login" ,'Success')   
#                         return redirect('/')
#                 else:
#                     cursor.close()
#                     if Flag == False:
#                         flash("In correct Email ! " ,"danger")
#                     else:
#                         flash("In correct Pasword ! ", "danger")
#     return render_template("login.html", form = form)
# @app.route("/logout")
# def logout():
#     session.pop("user_id" , None) # if no user id so no error , None will appear
#     return redirect('/login')

# if __name__ == "__main__":
#     app.run(debug=True)