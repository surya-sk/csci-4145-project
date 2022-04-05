import boto3
import json

with open("credentials.json") as f:
    creds_json = json.load(f)
Client_id = creds_json['user_pools_client_id']

def signup_user(email, username, password):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.sign_up(
        ClientId = Client_id,
        Username = username,
        Password = password,
        UserAttributes = [{'Name': 'email', 'Value': email}]
    )
    # return true if no error false otherwise
    return True

def verify_user(username, code):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.confirm_sign_up(
        ClientId = Client_id,
        Username = username,
        ConfirmationCode = code
    )

def login_user(username, password):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.initiate_auth(
        ClientId= Client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )

    access_token = response['AuthenticationResult']['AccessToken']
    response = client.get_user(
        AccessToken=access_token
    )
    if response['Username'] == username:
        return True
    else:
        return False

# password for test user account: Abcdef123!
