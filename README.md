# EC2_Autoshutdown
lambda function to shutdown idle EC2 instances for over 30 minuntes
To create a fucntion that automatically shuts down an EC2 instance when it's idle for more than 30 minutes, you can use a combination of AWS Lambda, CloudWatch Events, and IAM roles.
What we are going to do throughout this project

1. Creating IAM policy and Roles for lambda to stop and describe instances
2. Set Up AWS Lambda function
3. Create a Trigger with Event Rule 
4. Identify Idle Instances with a python script in the lambda function
5. Implement the Shutdown by checking the last time they was an activity in the instance and subtracting it from the current time, if its equal to 1800 seconds (30 mins)
6. Test and Monitor your lambda function
7. To create an AWS Lambda Function that automatically shuts down an EC2 instance when it's idle for more than 30 minutes, you can use a combination of **AWS Lambda** , CloudWatch Events, and IAM roles. Here's a high-level overview of the steps involved:

1. Head over to your AWS management console and search for IAM .
    
Create an IAM policy:On the pane at the left click policy, at the top right corner click create policy, select and open the json_policy file, copy and paste the **JSON** code snippet on policy editor.
Give a name to policy, review and create.
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:StopInstances",
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        }
    ]
}
2. Create an IAM Role for Lambda:Now lets head over and create an IAM role that allows Lambda to stop EC2 instances.
    
    Note: We selected Lambda as the Trusted entity and not EC2 because lambda here access the instance not the instance accessing the Lambda. 
    
    ![Screenshot 2023-10-19 at 18.29.52.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/59c8838b-7d1c-4ee0-b087-d5c2cf81eaa7/f26f4391-3352-4ba1-bbd1-3277891bd17c/Screenshot_2023-10-19_at_18.29.52.png)
    
    Still on left pane select ROLES and click create role at the top right corner, on next page select AWS service as trusted entity, under use case select Lambda.
    
     Attach the following policy you created earlier to the role, review and create role.
    
3. Create an AWS Lambda Function:
Now lets head over to the AWS lambda page, on your AWS management console page search for Lambda.
    
    Write a Lambda function in Python that will be triggered periodically by CloudWatch Events. This function will check the last activity time of your EC2 instance(s) and stop them if they have been idle for more than 1 hour.
    
    ```python
    import boto3
    import datetime
    
    def lambda_handler(event, context):
        ec2 = boto3.client('ec2')
    
        # Replace 'your-instance-id' with the ID of your EC2 instance
        instance_id = 'your-instance-id'
    
        # Get the instance's launch time
        response = ec2.describe_instances(InstanceIds=[instance_id])
        launch_time = response['Reservations'][0]['Instances'][0]['LaunchTime']
    
        # Calculate the current time
        current_time = datetime.datetime.now(launch_time.tzinfo)
    
        # Calculate the time difference
        time_difference = current_time - launch_time
    
        # If the instance has been idle for more than 1 hour, stop it
        if time_difference.total_seconds() > 3600:
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"EC2 instance {instance_id} has been stopped due to inactivity.")
        else:
            print(f"EC2 instance {instance_id} is still active.")
    
    ```
    
4. Create a Schedule using Event Bridge:
Create a schedule rule that triggers the Lambda function periodically ( every 15 minutes).
