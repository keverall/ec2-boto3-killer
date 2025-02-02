import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from datetime import datetime

def assume_role(account_id, role_name):
    sts_client = boto3.client('sts')
    try:
        response = sts_client.assume_role(
            RoleArn=f'arn:aws:iam::{account_id}:role/{role_name}',
            RoleSessionName='CrossAccountSession'
        )
        return response['Credentials']
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error assuming role: {e}")
        return None

def lambda_handler(event, context):
    
    central_account_id = 'central_account_id'
    role_name = 'CrossAccountRole'
    
    # Read target accounts from JSON file
    with open('../../cicd/ec2-scan/accounts.json') as f:
        target_accounts = json.load(f)['accounts']
        
    sns_topic_arn = 'arn:aws:sns:region:account-id:topic-name'
    sns_client = boto3.client('sns')


    for target_account_id in target_accounts:
        credentials = assume_role(target_account_id, role_name)
        if not credentials:
            continue

        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        try:
            # Scan for EIPs without an allocation ID
            eips = ec2_client.describe_addresses()
            eips_to_remove = []
            for eip in eips['Addresses']:
                if 'AllocationId' not in eip:
                    eips_to_remove.append(eip)

            # Remove EIPs and collect details for SNS message
            removed_eips_details = []
            for eip in eips_to_remove:
                ec2_client.release_address(AllocationId=eip['AllocationId'])
                eip_details = {
                    'PublicIp': eip['PublicIp'],
                    'InstanceId': eip.get('InstanceId', 'N/A'),
                    'Tags': eip.get('Tags', [])
                }
                removed_eips_details.append(eip_details)

            # Send SNS message with details of removed EIPs
            if removed_eips_details:
                message = f"Removed EIPs in account {target_account_id}:\n"
                for eip in removed_eips_details:
                    message += f"PublicIp: {eip['PublicIp']}, InstanceId: {eip['InstanceId']}, Tags: {eip['Tags']}\n"
                sns_client.publish(
                    TopicArn=sns_topic_arn,
                    Subject=f"EIP Cleanup Report for Account {target_account_id}",
                    Message=message
                )
        except ClientError as e:
            print(f"Error processing account {target_account_id}: {e}")