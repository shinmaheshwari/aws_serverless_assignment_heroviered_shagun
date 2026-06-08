import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Extract instance ID from the event
    instance_id = event['detail']['instance-id']

    # Current date
    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    # Create tags
    tags = [
        {
            'Key': 'LaunchDate',
            'Value': current_date
        },
        {
            'Key': 'Environment',
            'Value': 'Development'
        }
    ]

    # Apply tags to instance
    ec2.create_tags(
        Resources=[instance_id],
        Tags=tags
    )

    # Confirmation log
    print(f"Successfully tagged instance {instance_id}")
