import json
import boto3

access_key = 'AKIA4I7AUGAGW3FOIMXN'
secret_key = '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'

def upload_file(username, file_name, blocks, folder_name):
    client = boto3.client('s3', aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)

    bucket = '4145project'
    file_key = username + '/' + folder_name + '/image'
    response = client.upload_file(file_name, Bucket=bucket, Key=file_key)
    print(response)

    file_key = username + '/' + folder_name + '/textractObj'
    response = client.put_object(Bucket=bucket, Key=file_key, Body=(bytes(json.dumps(blocks).encode('UTF-8'))))
    print(response)