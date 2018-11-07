from flask import Flask, flash, render_template, request, redirect, session, url_for
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'(?=.*[A_Z])(?=.*\d).+$')
BIRTH_REGEX = re.compile(r'^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$')

app = Flask(__name__, static_url_path='')

app.secret_key = 'nosecretshere'

@app.route('/', methods=['get'])

def index():
    return render_template('index.html')

@app.route('/process', methods=['post'])
def process():
    if len(request.form['firstname']) < 1 or len(request.form['lastname']) < 1 or len(request.form['email']) < 1 or len(request.form['password']) < 1 or len(request.form ['cpassword']) < 1:
        flash("Make sure all fields are filled")
    elif  not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
    elif len(request.form['password']) < 8 or len(request.form['cpassword']) < 8:
        flash("Password must be at least 8 characters")
    elif not NAME_REGEX.match(request.form['firstname']) or not NAME_REGEX.match(request.form ['lastname']):
        flash("Name must not contain any numbers!")
    elif request.form['password'] != request.form['cpassword']:
        flash("Passwords do not match!")
    elif not PASSWORD_REGEX.match(request.form['password']) or not PASSWORD_REGEX.match (request.form['cpassword']):
        flash("Password must contain at least one uppercase letter and one numeric value")
    elif not BIRTH_REGEX.match(request.form['birthdate']):
        flash("Invalid date, must be in form: mm/dd/yyyy")
    else:
        flash("Congratulations, you're in!")
    session['firstname'] = request.form['firstname']
    session['lastname'] = request.form['lastname']
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    session['cpassword'] = request.form['cpassword']
    session['birthdate'] = request.form['birthdate']
    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)