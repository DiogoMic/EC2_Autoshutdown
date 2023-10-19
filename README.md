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
