import boto3

def signup_user(email, username, password):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.sign_up(
        ClientId = '6603uqjecfj36n3r9r7pk5m9q',
        Username = username,
        Password = password,
        UserAttributes = [{'Name': 'email', 'Value': email}]
    )
    # return true if no error false otherwise
    return True

def verify_user(username, code):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.confirm_sign_up(
        ClientId = '6603uqjecfj36n3r9r7pk5m9q',
        Username = username,
        ConfirmationCode = code
    )

def login_user(username, password):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.initiate_auth(
        ClientId='6603uqjecfj36n3r9r7pk5m9q',
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

#Abcdef123!
