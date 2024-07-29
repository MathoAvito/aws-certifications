# AWS Lambda Exercise: Monitor and Stop EC2 Instances

This exercise demonstrates how to create an AWS Lambda function that:
1. Sends an email with the status of all running and stopped EC2 instances whenever it is manually triggered.
2. Stops all running EC2 instances if the function is triggered between 8 PM and 12 AM. Outside of this time window, it only sends the status.

## Steps Overview

### 1. Create an SNS Topic
We created an Amazon SNS topic to send email notifications about the status of EC2 instances. An email subscription to this topic ensures you receive updates.

### 2. Create an IAM Role for Lambda
An IAM role with the necessary permissions was created to allow the Lambda function to describe and stop EC2 instances, and to publish messages to the SNS topic.

### 3. Create a GitHub Repository
A GitHub repository was set up to store the Lambda function code (`ec2_status_stop.py`), facilitating version control and collaboration.

### 4. Create the Lambda Function
We created a Lambda function in the AWS Management Console, using the code from the `ec2_status_stop.py` file. This function checks the status of EC2 instances and stops them if triggered between 8 PM and 12 AM.

### 5. Set Up a CloudWatch Event Rule
A CloudWatch Event Rule was configured to trigger the Lambda function hourly. This ensures the function runs automatically and checks if the time falls within the specified window to stop instances.

### 6. Add Tags to Resources
Tags were added to all created resources (Lambda function and SNS topic) with the key `Project` and value `AWSDeveloperHandsOn`. This helps in organizing and managing resources related to this exercise.

## Lambda Function Code

The Lambda function code is provided in the file [`ec2_status_stop.py`](./ec2_status_stop.py).

### Triggering the Function

- **Automatic Trigger:** The function is triggered hourly by a CloudWatch Event Rule.
- **Manual Trigger:** You can manually trigger the function through the AWS Management Console or AWS CLI.

#### Manual Trigger via AWS Management Console

1. **Navigate to AWS Lambda.**
2. **Select your Lambda function.**
3. **Click on "Test".**
4. **Configure a new test event:**
   - **Event template:** Use the "Hello World" template or any suitable template.
   - **Event name:** Provide a name for the test event (e.g., `ManualTriggerEvent`).
   - **Event JSON:**
     ```json
     {
       "source": "manual"
     }
     ```
5. **Click "Create" to save the test event.**
6. **Click "Test"** to manually trigger the function.

#### Manual Trigger via AWS CLI

```sh
aws lambda invoke --function-name EC2StatusAndStopFunction output.txt
