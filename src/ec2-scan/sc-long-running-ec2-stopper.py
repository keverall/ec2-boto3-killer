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

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    stopped_instances = kill_all(ec2, response)

    return {
        'statusCode': 200,
        'body': {
            'message': 'Instances stopped successfully',
            'stopped_instances': stopped_instances
        }
    }