import json
import boto3

with open("credentials.json") as f:
    creds_json = json.load(f)
access_key = creds_json['s3_access_key']
secret_key = creds_json['s3_secret_key']

def upload_file(username, file_name, blocks, folder_name, temp=False):
    client = boto3.client('s3', aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)

    bucket = '4145project'
    if temp:
        file_key = username + '/' + folder_name + '/temp'
        response = client.upload_file(file_name, Bucket=bucket, Key=file_key)
        return file_key
    else:
        file_key = username + '/' + folder_name + '/image'
        response = client.upload_file(file_name, Bucket=bucket, Key=file_key)

        file_key = username + '/' + folder_name + '/textractObj'
        response = client.put_object(Bucket=bucket, Key=file_key, Body=(json.dumps(blocks)))

        return response

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

    textract_obj = s3_client.get_object(Bucket='4145project', Key=username + '/' + file + '/textractObj')
    textract_obj = json.loads(textract_obj['Body'].read().decode('utf-8'))
    textract_obj = textract_obj['body']
    print(textract_obj)
    print(type(textract_obj))
    textract_obj = json.loads(textract_obj)

    del textract_obj[0]   # the first element describes the size of the page. This is not relevant to our application

    return textract_obj

