from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import InputRequired, Email, Length
import os
import boto3
import textract_wrapper
from s3_functions import upload_file

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
    file_name = form.filename.data
    file_name = str(file_name)

    global user
    mkdir = 'photos/' + user
    if not os.path.exists(mkdir):
        os.makedirs(mkdir)
    print(request.files.to_dict(flat=False))
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            file_name = './photos/' + user + '/' + file_name + '.jpg'
            photo.save(file_name)
            session = boto3.Session(
                aws_access_key_id="ASIAXL2JPQZPE6GC2BXA",
                aws_secret_access_key="zXJbluvVqaNQ+flvEsveWTnyhSFqUi1hCC1RlP9J",
                aws_session_token="FwoGZXIvYXdzENH//////////wEaDLtcNupZxgkt6ivKyCLAAbUV9pxZ+/tlqzHkl07iLmm+w/5qKvS0rb7JjJjb/5JK/9kHY0ZFewf7tWea39fuB6OwZKEhSF6CDgMXsnGMv2O1p3qySOdriJ7ub2lRPxvdP8o9d8CWmaNdzVzn6Vt0w2O+5doGwkJIBcIO1Odvik8TFN63DMoifQLZyN5ZUbQFDgyOXhyX9qDbydkRihdT/WQ3OwMkqg0ghtPjCzq9NA2hVLAb8tRUKHjseRvMQ3rO1lghEWUby34eaulbPVR8Wiik/OyRBjIt1YP8CoC+HMfSKCVC1BLRLrGP2OiKH7PQMrHCUDApK0bO+K6Il4AW2iqyUAER",
                region_name='us-east-1'
                )
            client = session.client('textract')
            textract = textract_wrapper.TextractWrapper(client, None, None)
            response = textract.detect_file_text(document_file_name=file_name)
            #for item in response['Blocks']:
            #    if item["BlockType"] == "LINE":
            #        print('\033[92m' + item['Text'] + '\033[92m')
            blocks = response['Blocks']
            upload_file(user, file_name, blocks, str(form.filename.data))
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
