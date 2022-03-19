from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import InputRequired, Email, Length
import os
import boto3
import textract_wrapper

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

class UploadFileForm(FlaskForm):
    filename = StringField('filename', validators=[InputRequired()])
    file = FileField('file')

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

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadFileForm()
    print(request.files.to_dict(flat=False))
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            filename = os.path.join("C:/Users/surya/OneDrive/Desktop", "pic.jpg")
            photo.save(filename)
            session = boto3.Session(
                aws_access_key_id="ASIAXL2JPQZPPQY23EGL",
                aws_secret_access_key="vwhSeW5VNNphCrSzCN6dw24SbfVDVrHaQlKWsJB5",
                aws_session_token="FwoGZXIvYXdzEHMaDPWrjtUT9+h+LUA/mSLAAXs0ysYHkSEKxwlu3uPJ37XqoTEGrwxrPX/mZ2i8r+UTN8yLrMxkYmSEXuF6bAtYrx7hbJa0jDwOE2lv16RYUK0QiQFc3qWdSt5weUVO+KqUi6hgSGcJDCdBbPIFhinDSL6qvoZH5LgXU1cKlyV9clPaKBrkFkiV/yVFEpiYEiL8uGyWEiP5wRVn57lwO13S25rshSXH25XIg7qDh//O5LeoP7etD9bWwzNfRfezzOTZD/Wnb7mLEHHC2mjfnKcvPSicrNiRBjIt8LVwFT6W2AQBKqGYmj1os33W1wwGyUBDKj5k+aDYCLNecr5McqvziZRxh8v1",
                region_name='us-east-1'
                )
            client = session.client('textract')
            textract = textract_wrapper.TextractWrapper(client, None, None)
            response = textract.detect_file_text(document_file_name=filename)
            for item in response['Blocks']:
                if item["BlockType"] == "LINE":
                    print('\033[92m' + item['Text'] + '\033[92m')
    return render_template('upload.html', form=form)

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
