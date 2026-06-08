import boto3

elb = boto3.client('elbv2')
sns = boto3.client('sns')

# Replace with your SNS Topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:562904760755:ELBHealthAlerts'

def lambda_handler(event, context):

    unhealthy_instances = []

    # Get all target groups
    target_groups = elb.describe_target_groups()

    for tg in target_groups['TargetGroups']:

        target_group_arn = tg['TargetGroupArn']
        target_group_name = tg['TargetGroupName']

        # Get target health
        health = elb.describe_target_health(
            TargetGroupArn=target_group_arn
        )

        for target in health['TargetHealthDescriptions']:

            instance_id = target['Target']['Id']
            state = target['TargetHealth']['State']

            print(f"Instance: {instance_id} | State: {state}")

            if state != 'healthy':

                unhealthy_instances.append({
                    'InstanceId': instance_id,
                    'State': state,
                    'TargetGroup': target_group_name
                })

    # Send SNS alert if unhealthy instances found
    if unhealthy_instances:

        message = "Unhealthy Instances Detected:\n\n"

        for instance in unhealthy_instances:
            message += (
                f"Instance ID: {instance['InstanceId']}\n"
                f"Health State: {instance['State']}\n"
                f"Target Group: {instance['TargetGroup']}\n\n"
            )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='ELB Unhealthy Instance Alert',
            Message=message
        )

        print("SNS alert sent successfully.")

    else:
        print("All instances are healthy.")

    return {
        'statusCode': 200,
        'body': 'ELB Health Check Completed'
    }
