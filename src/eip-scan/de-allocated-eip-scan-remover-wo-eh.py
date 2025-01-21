import boto3
from datetime import datetime

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
    sns_topic_arn = 'arn:aws:sns:region:account-id:topic-name'
    sns_client = boto3.client('sns')

    for account_id in target_accounts:
        credentials = assume_role(account_id, role_name)
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

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
            message = f"Removed EIPs in account {account_id}:\n"
            for eip in removed_eips_details:
                message += f"PublicIp: {eip['PublicIp']}, InstanceId: {eip['InstanceId']}, Tags: {eip['Tags']}\n"
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject=f"EIP Cleanup Report for Account {account_id}",
                Message=message
            )