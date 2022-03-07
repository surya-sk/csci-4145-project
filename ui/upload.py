import os
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

@app.route("/")
def showUploadPage():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run()