import boto3
import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Replace 'your-instance-id' with the ID of your EC2 instance
    instance_id = 'i-02a118bd1b80146cb'

    # Get the instance's launch time
    response = ec2.describe_instances(InstanceIds=[instance_id])
    launch_time = response['Reservations'][0]['Instances'][0]['LaunchTime']

    # Calculate the current time
    current_time = datetime.datetime.now(launch_time.tzinfo)

    # Calculate the time difference
    time_difference = current_time - launch_time

    # If the instance has been idle for more than 30 minutes, stop it
    if time_difference.total_seconds() > 1800:
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"EC2 instance {instance_id} has been stopped due to inactivity.")
    else:
        print(f"EC2 instance {instance_id} is still active.")
