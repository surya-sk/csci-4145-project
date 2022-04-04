import json
import boto3
from boto3.session import Session
import matplotlib.image as mpimg
import io
import cv2
from PIL import Image

access_key = 'AKIA4I7AUGAGW3FOIMXN'
secret_key = '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'

def upload_file(username, file_name, blocks, folder_name):
    client = boto3.client('s3', aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)

    bucket = '4145project'
    file_key = username + '/' + folder_name + '/image'
    response = client.upload_file(file_name, Bucket=bucket, Key=file_key)

    file_key = username + '/' + folder_name + '/textractObj'
    response = client.put_object(Bucket=bucket, Key=file_key, Body=(bytes(json.dumps(blocks).encode('UTF-8'))))

def get_files(username):
    client = boto3.client('s3', aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key, region_name='us-east-1')
    bucket = '4145project'
    prefix = username + '/'
    result = client.list_objects(Bucket=bucket, Prefix=prefix)['Contents']
    files = []
    for document in result:
        docName = str(document['Key'])
        docName = docName.replace(prefix, '')
        folderName = docName.split('/')
        folderName = folderName[0]
        if folderName not in files:
            files.append(folderName)
    return files

def getS3File(username, file):
    s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name='us-east-1')

    response = s3_client.download_file(Bucket='4145project', Key=username + '/' + file + '/image', Filename= 'static/' + username + 'image.jpg')

