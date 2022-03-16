from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

from user_pool_functions import signup_user, verify_user, login_user

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'SeCrEtKeY'

user = ''
signedUp = False

class SignUpForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email')])
    username = StringField('username', validators=[InputRequired()])
    # password min-length is set to 8 characters in user pools
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=50)])

class SignUpVerificationForm(FlaskForm):
    code = StringField('code', validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=50)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        if signup_user(email, username, password):
            global user
            user = username
            return redirect(url_for('verify'))

    return render_template('signup.html', form=form, variable=signedUp)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form = SignUpVerificationForm()
    if form.validate_on_submit():
        code = form.code.data
        global user
        verify_user(user, code)
    return render_template('verify_signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if login_user(username, password):
            global user
            user = username
            return redirect(url_for('upload'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
