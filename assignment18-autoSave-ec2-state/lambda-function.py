import boto3
import json
from datetime import datetime

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

BUCKET_NAME = 'ec2-backup-assignment18'

def lambda_handler(event, context):

    # Get instance ID from event
    instance_id = event['detail']['instance-id']

    print(f"Instance Terminated: {instance_id}")

    # Fetch instance details
    response = ec2.describe_instances(
        InstanceIds=[instance_id]
    )

    instance = response['Reservations'][0]['Instances'][0]

    # Create backup data
    instance_data = {
        'InstanceId': instance.get('InstanceId'),
        'InstanceType': instance.get('InstanceType'),
        'AMI_ID': instance.get('ImageId'),
        'LaunchTime': str(instance.get('LaunchTime')),
        'State': instance.get('State')['Name'],
        'AvailabilityZone': instance['Placement']['AvailabilityZone']
    }

    # Convert to JSON
    json_data = json.dumps(instance_data, indent=4)

    # File name
    file_name = f"{instance_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    # Upload to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json_data
    )

    print(f"Backup saved to S3: {file_name}")

    return {
        'statusCode': 200,
        'body': f'Successfully backed up {instance_id}'
    }
