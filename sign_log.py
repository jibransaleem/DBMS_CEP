# from flask import Flask, render_template, request, url_for, redirect, session
# from database import Config  
# from flask_mysqldb import MySQL
# from forms import RegisterUser, LoginUser
# import bcrypt

# app = Flask(__name__, template_folder='templates')

# # Setting up database
# app.config.from_object(Config)
# app.secret_key = '123'

# # Database object
# mysql = MySQL(app)

# @app.route("/", methods=['GET', 'POST'])
# def Register():
#     form = RegisterUser()
#     if form.validate_on_submit():
#         name = form.name.data
#         mail = form.email.data
#         password = form.password.data
#         hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#         option = form.option.data        
#         cursor = mysql.connection.cursor()

#         if option == 'Employee':
#             cursor.execute("SELECT email FROM Employee WHERE email = %s", (mail,))
#             existing_email = cursor.fetchone()
#             if existing_email:
#                 cursor.close()
#                 return "Email already taken"

#             cursor.execute("INSERT INTO Employee (name, email, password) VALUES (%s, %s, %s)", (name, mail, hashed_password))
#             mysql.connection.commit()
#             cursor.close()
#             return redirect(url_for('home'))
        
#         else:
#             cursor.execute("INSERT INTO Company (name, email, password) VALUES (%s, %s, %s)", (name, mail, hashed_password))
#             mysql.connection.commit()
#             cursor.close()
#             return redirect(url_for('home'))

#     return render_template("signup.html", form=form)


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginUser()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#         option = form.option.data        
#         cursor = mysql.connection.cursor()

#         if option == 'Employee':
#             cursor.execute("SELECT email, password FROM Employee WHERE TRIM(email) = %s", (email.strip(),))
#             data = cursor.fetchone()
#             if data and bcrypt.checkpw(password.encode('utf-8'), data[1].encode('utf-8')):
#                 session['user_id'] = data[0]
#                 cursor.close()
#                 return render_template('emp.html')
#             else:
#                 return (f'ROLE IS {option}')
#         elif option == 'Company':
#             cursor.execute("SELECT email, password FROM Company WHERE TRIM(email) = %s", (email.strip(),))
#             data = cursor.fetchone()
#             if data and bcrypt.checkpw(password.encode('utf-8'), data[1].encode('utf-8')):
#                 session['user_id'] = data[0]
#                 cursor.close()
#                 return render_template('company.html')
#             else:
#                 return "company m msla"
#         else:
#             return f'{data}'
#     return render_template("login.html", form=form)


# @app.route("/home")
# def home():
#     return render_template("home.html")


# if __name__ == "__main__":
#     app.run(debug=True)
