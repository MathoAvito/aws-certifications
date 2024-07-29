import boto3
import json
from datetime import datetime
import pytz

# Initialize clients
ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')

# SNS topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:REGION:CCOUNT_ID:SNSTOPIC_NAME'
TIMEZONE = 'TIMEZONE'  # e.g., 'US/Eastern'

def lambda_handler(event, context):
    # Get all instances
    response = ec2_client.describe_instances()
    instances = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            instances.append((instance_id, state))
    
    # Create the email message
    message = "EC2 Instance Status:\n\n"
    for instance_id, state in instances:
        message += f"Instance ID: {instance_id}, State: {state}\n"
    
    # Get the current time in the specified timezone
    now = datetime.now(pytz.timezone(TIMEZONE))
    current_hour = now.hour
    
    # Check if the function is triggered within the specified time window
    if 20 <= current_hour <= 23 or current_hour == 0:
        # Stop all running instances
        running_instances = [i[0] for i in instances if i[1] == 'running']
        if running_instances:
            ec2_client.stop_instances(InstanceIds=running_instances)
            stop_message = f"Stopped instances: {', '.join(running_instances)}"
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject='EC2 Instances Stopped',
                Message=stop_message
            )
            message += "\n\n" + stop_message
    
    # Send the email via SNS
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject='EC2 Instance Status',
        Message=message
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Function executed successfully')
    }
