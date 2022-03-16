import os
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

@app.route("/")
def showUploadPage():
    return render_template('upload.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    print(request.files.to_dict(flat=False))
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            photo.save(os.path.join("C:/Users/surya/OneDrive/Desktop", "pic.jpg"))
    return redirect(url_for('showUploadPage'))

if __name__ == '__main__':
    app.run()