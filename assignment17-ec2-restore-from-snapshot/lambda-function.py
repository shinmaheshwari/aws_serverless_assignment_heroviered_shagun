import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Get all running instances
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    # Pick first running instance
    instance = response['Reservations'][0]['Instances'][0]

    instance_id = instance['InstanceId']
    ami_id = instance['ImageId']
    availability_zone = instance['Placement']['AvailabilityZone']

    print(f"Source Instance ID: {instance_id}")
    print(f"AMI ID: {ami_id}")

    # Get root EBS volume ID
    volume_id = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']

    print(f"Volume ID: {volume_id}")

    # Fetch snapshots of the volume
    snapshots = ec2.describe_snapshots(
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume_id]
            }
        ],
        OwnerIds=['self']
    )

    snapshot_list = snapshots['Snapshots']

    # Sort snapshots by latest
    snapshot_list.sort(
        key=lambda x: x['StartTime'],
        reverse=True
    )

    latest_snapshot = snapshot_list[0]
    snapshot_id = latest_snapshot['SnapshotId']

    print(f"Latest Snapshot ID: {snapshot_id}")

    # Create new volume from snapshot
    new_volume = ec2.create_volume(
        SnapshotId=snapshot_id,
        AvailabilityZone=availability_zone,
        VolumeType='gp2'
    )

    new_volume_id = new_volume['VolumeId']

    print(f"New Volume Created: {new_volume_id}")

    # Launch new EC2 instance
    new_instance = ec2.run_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        Placement={
            'AvailabilityZone': availability_zone
        }
    )

    new_instance_id = new_instance['Instances'][0]['InstanceId']

    print(f"New EC2 Instance Created: {new_instance_id}")

    return {
        'statusCode': 200,
        'body': f'New EC2 Instance Created: {new_instance_id}'
    }
