import boto3
from datetime import datetime, timezone

def stop_instances(client, instance_id, stopped_instances):
    response = client.stop_instances(
        InstanceIds=[
            instance_id
        ],
    )
    print(f'Stopped instance: {instance_id}')
    print(response)
    stopped_instances.append(instance_id)

def kill_all(client, response):
    stopped_instances = []
    current_time = datetime.now(timezone.utc)
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"] == 'running':
                launch_time = instance["LaunchTime"]
                running_for = int((current_time - launch_time).total_seconds())
                if running_for > 14400:
                    tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    if tags.get('live') == 'no':
                        stop_instances(client, instance["InstanceId"], stopped_instances)
    return stopped_instances

def send_sns_message(stopped_instances, account_id, account_name):
    sns_client = boto3.client('sns')
    topic_arn = 'arn:aws:sns:region:account-id:topic-name'  # Replace with your actual SNS topic ARN
    message = (
        f"At {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}, "
        f"the following EC2 instances were stopped in AWS account {account_id} ({account_name}):\n"
        f"{', '.join(stopped_instances)}"
    )
    sns_client.publish(
        TopicArn=topic_arn,
        Subject='EC2 Instances Stopped',
        Message=message
    )

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sts_client = boto3.client('sts')
    account_id = sts_client.get_caller_identity()["Account"]
    account_name = boto3.client('organizations').describe_account(AccountId=account_id)['Account']['Name']

    response = ec2.describe_instances()
    stopped_instances = kill_all(ec2, response)

    if stopped_instances:
        send_sns_message(stopped_instances, account_id, account_name)

    return {
        'statusCode': 200,
        'body': {
            'message': 'Instances stopped successfully',
            'stopped_instances': stopped_instances
        }
    }