from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import InputRequired, Email, Length
import os
import boto3
from s3_functions import upload_file, get_files, getS3File
import json
from PIL import Image

from user_pool_functions import signup_user, verify_user, login_user

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'SeCrEtKeY'

AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
AWS_SESSION_TOKEN = ""

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
    global user
    file_list = get_files(user)

    form = UploadFileForm()
    file_name = form.filename.data
    file_name = str(file_name)

    mkdir = 'photos/' + user
    if not os.path.exists(mkdir):
        os.makedirs(mkdir)

    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            image = Image.open(photo)
            image.convert("RGB")
            file_name = './photos/' + user + '/' + file_name + '.jpg'
            image.save(file_name)
            key = upload_file(user, file_name, None, str(form.filename.data), True)

            session = boto3.Session(
                aws_access_key_id=creds_json['s3_access_key'],
                aws_secret_access_key=creds_json['s3_secret_key'],
                region_name='us-east-1'
                )

            client = session.client('lambda')
            input = {"user": user, "file": str(form.filename.data)}
            response = client.invoke(FunctionName='get_text', InvocationType='RequestResponse', Payload=json.dumps(input))
            data = response['Payload'].read()
            blocks = json.loads(data.decode('utf-8'))

            upload_file(user, file_name, blocks, str(form.filename.data))
            file_list = get_files(user)
    return render_template('upload.html', form=form, file_list=file_list)

@app.route('/showFile', methods=['GET'])
def show_file():
    file = request.args.get('file')
    global user
    textract_object = getS3File(user, file)
    return render_template('show_file.html', user=user, textract_object=textract_object)

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
    with open("credentials.json") as f:
        creds_json = json.load(f)
    AWS_ACCESS_KEY = creds_json['access_key']
    AWS_SECRET_KEY = creds_json['secret_key']
    AWS_SESSION_TOKEN = creds_json['session_token']
    app.run(debug=True, port=3000, host='0.0.0.0')
