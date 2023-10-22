<img width="797" alt="Screenshot 2023-10-21 at 21 16 36" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/924c6338-704a-4537-8db4-92619f652738">



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

2. Create an IAM Role for Lambda:Now lets head over and create an IAM role that allows Lambda to stop EC2 instances.
    
    Note: We selected Lambda as the Trusted entity and not EC2 because lambda here access the instance not the instance accessing the Lambda. 
    
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
<img width="277" alt="Screenshot 2023-10-19 at 18 23 04" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/2681f991-940f-4ac9-b8dd-b9cadb6e6811">

Name Your Schedule 

<img width="829" alt="Screenshot 2023-10-19 at 18 23 17" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/7fccb3f4-3505-42b7-8223-718fefc2cab4">

In schedule pattern under occurrence select recurring schedule.

Under schedule type select rate based schedule.


<img width="826" alt="Screenshot 2023-10-19 at 18 24 11" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/663fe26f-627e-46b8-9d0a-2ff6f55f30f0">

Here you set the time for the to start and stop

<img width="835" alt="Screenshot 2023-10-19 at 18 24 42" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/18168655-ceda-492d-8c17-30f41e4474f2">

Now we will select the target, the target which the eventbridge schedule invoke will be Lambda

<img width="891" alt="Screenshot 2023-10-19 at 18 25 44" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/2f91c742-3cd2-4b59-aca0-12b4466f110b">

Under Lambda function select the function you created earlier.

<img width="823" alt="Screenshot 2023-10-19 at 18 26 08" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/d8712c91-bf2e-4980-9be6-45f4ae4e7d8e">

In settings under enable state toggle it to enable.

<img width="847" alt="Screenshot 2023-10-19 at 18 26 39" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/a25d112f-ede7-4eac-b2a9-453627b72fce">

Under permission in execution role select “Create new role for this schedule”, this role will allow eventbridge scheduler to send events to the target we selected.

<img width="821" alt="Screenshot 2023-10-19 at 18 26 59" src="https://github.com/McTello/EC2_Autoshutdown/assets/89931817/6f366a19-86dd-4ad1-a21d-3b293d9e9e78">


Review and create!!!.
