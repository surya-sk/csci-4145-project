from fileinput import filename
import os
import boto3
from flask import Flask, request, render_template, url_for, redirect
import sys
sys.path.append('../csci-4145-project')
import textract_wrapper

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
            filename = os.path.join("C:/Users/surya/OneDrive/Desktop", "pic.jpg")
            session = boto3.Session(
                aws_access_key_id="ASIAXL2JPQZPFCR5F3VF",
                aws_secret_access_key="GX/v0sWSISHgTRv4a/GJNcf+1R2htliF25P91GHG",
                aws_session_token="FwoGZXIvYXdzECcaDEdBSBkPrIWY+4OZsyLAAS9tqCtpvUn4v6yym/2iXsJSTO7qwrWBw9IrmOtM1TUqecufKPMpe+4xiz+Ob1F4erdWniwN8wtUP9q8LCGv45jBIpOi6BAGl5jPyX4pze10BpV2/B+8pEDegMc9ZwDWJp2GWp7GJQPCgCgbnwoJENBaB2ntFSZOmZnqtSozcDwAWpfflfNXwPcQ+nZ+d7h6QMrHroowbXHpYxXw1Dk13GDt4GN1OYClEF/8vHU4YT1r1uOrOCMn/dIzUTTqmwMV8yjF0MeRBjItv8zgx0YmGUOe1n1PblsvbUOSWlTjiUitUKUO+p14pzKwm+tJQcMFWNSxaM9m",
                region_name='us-east-1'
                )
            client = session.client('textract')
            textract = textract_wrapper.TextractWrapper(client, None, None)
            response = textract.detect_file_text(document_file_name=filename)
            for item in response['Blocks']:
                if item["BlockType"] == "LINE":
                    print('\033[92m' + item['Text'] + '\033[92m')
    return redirect(url_for('showUploadPage'))

if __name__ == '__main__':
    app.run()