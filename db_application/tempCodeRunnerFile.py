from flask import Flask, render_template, request, url_for, redirect, session
from database import Config  
from flask_mysqldb import MySQL
from forms import RegisterUser
import bcrypt

app = Flask(__name__, template_folder='templates')

# Setting up database
app.config.from_object(Config)
app.secret_key = '123'

# Database object
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        # Process form data
        pass
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
