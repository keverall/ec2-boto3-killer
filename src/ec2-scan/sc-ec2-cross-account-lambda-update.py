## Lambda Function Update

# Update Lambda function to assume the cross-account role before performing actions on the target accounts.


import boto3
from datetime import datetime, timedelta

def assume_role(account_id, role_name):
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn=f'arn:aws:iam::{account_id}:role/{role_name}',
        RoleSessionName='CrossAccountSession'
    )
    return response['Credentials']

def lambda_handler(event, context):
    central_account_id = 'central_account_id'
    role_name = 'CrossAccountRole'
    target_accounts = ['account_id_1', 'account_id_2']

    for account_id in target_accounts:
        credentials = assume_role(account_id, role_name)
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        # Your existing code to stop instances
        # ...
# this setup ensures that your Lambda function in the central account
# can assume roles in the target accounts 
# and perform the necessary EC2 actions.