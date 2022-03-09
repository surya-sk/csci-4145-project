import boto3

def signup_user(email, username, password):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.sign_up(
        ClientId = '6603uqjecfj36n3r9r7pk5m9q',
        Username = username,
        Password = password,
        UserAttributes = [{'Name': 'email', 'Value': email}]
    )
    print(response)
    # return true if no error false otherwise
    return True

def verify_user(username, code):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.confirm_sign_up(
        ClientId = '6603uqjecfj36n3r9r7pk5m9q',
        Username = username,
        ConfirmationCode = code
    )