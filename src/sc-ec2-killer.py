import boto3
from datetime import datetime, timedelta

client = boto3.client('ec2')

ec2 = boto3.resource('ec2', region_name='instance_region_name')
volume = ec2.Volume('vol-id')

print (volume.create_time.strftime("%Y-%m-%d %H:%M:%S"))
ec2_uptime = volume.create_time.strftime("%Y-%m-%d %H:%M:%S")

# Get the current time
current_time = datetime.now()

# Calculate the difference in seconds
runningFor = int((current_time - ec2_uptime).total_seconds())

if runningFor > 14400:
    ec2.Client.stop_instances(**kwargs)

# Format the current time using strftime
formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

response = client.stop_instances(


print(response)

for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"] == 'running':
               print(instance["InstanceId"], instance["State"]["Name"])
               print (volume.create_time.strftime("%Y-%m-%d %H:%M:%S"))
               ec2_uptime = volume.create_time.strftime("%Y-%m-%d %H:%M:%S")
               runningFor = int((current_time - ec2_uptime).total_seconds())
               if runningFor > 14400:
                   InstanceIds=[instance["InstanceId"]],


)
                   
               
import boto3

def stop_instances(client, instance_id):
    response = ec2.stop_instances(
        InstanceIds=[
            instance_id
            ],
        )
    
def kill_all():
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"] == 'running':
                if instance["InstanceId"] != ide_id:
                        stop_instances(ec2, instance["InstanceId"])

def main():
    kill_all()
ec2 = boto3.client('ec2')

ide_id = 'i-0cd54c8eee80de55c'

response = ec2.describe_instances()

if __name__ == '__main__':
    main()
    