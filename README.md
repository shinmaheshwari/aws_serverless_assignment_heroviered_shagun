# AWS Serverless Assignment – Shagun Maheshwari

## 📌 Overview
This project demonstrates AWS automation using **Lambda and Boto3**.

The assignment focuses on:
- Automating EC2 instance management
- Managing S3 buckets
- Monitoring security (S3 encryption)
- Automating EBS snapshots

---

## 🛠️ Technologies Used
- AWS Lambda (Python 3.x)
- Boto3 (AWS SDK)
- EC2, S3, EBS
- IAM Roles
- CloudWatch Logs

---

# ✅ Assignment 1: EC2 Auto Start/Stop

## 🎯 Objective
Automatically start and stop EC2 instances based on tags.

---

## ⚙️ Steps Followed

### 1. EC2 Setup
- Created 2 EC2 instances:
  - Instance 1 → `Action = Auto-Stop`
  - Instance 2 → `Action = Auto-Start`

---

### 2. IAM Role
Created role: lambda-ec2-management-role

Attached policies:
- AmazonEC2FullAccess
- AWSLambdaBasicExecutionRole

---

### 3. Lambda Setup
- Function Name: `ec2-auto-start-stop`
- Runtime: Python 3.x
- Timeout: **15 seconds**
- Memory: 128 MB

---

### 4. Lambda Code

```python
import boto3

def lambda_handler(event, context):
    print("Lambda execution started")

    ec2 = boto3.client('ec2')

    # Stop instances
    stop_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    stop_ids = [i['InstanceId'] for r in stop_instances['Reservations'] for i in r['Instances']]
    print("Auto-Stop Found:", stop_ids)

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print("Stopped:", stop_ids)

    # Start instances
    start_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )

    start_ids = [i['InstanceId'] for r in start_instances['Reservations'] for i in r['Instances']]
    print("Auto-Start Found:", start_ids)

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print("Started:", start_ids)

    print("Execution complete")
    return "Success"


🧪 Testing

Manually triggered Lambda using test event {}
Verified EC2 states changed as expected


✅ Output

Instances with Auto-Stop were stopped
Instances with Auto-Start were started
Verified using:

EC2 dashboard
CloudWatch logs




⚠️ Issues Faced & Fixes
1. Timeout Error
Error:
Task timed out after 3.01 seconds

Fix:

Increased timeout to 15 seconds


2. Missing CloudWatch Logs
Issue:
No logs were visible
Fix:
Added policy:
AWSLambdaBasicExecutionRole


3. Logs Not Showing Output
Cause:
Instances already in correct state
Fix:

Changed instance state manually
Added debug print statements


📸 Screenshots
EC2 Instances (Before & After)
screenshots/ec2-before.png
screenshots/ec2-after.png
Lambda Configuration
screenshots/lambda-config.png
CloudWatch Logs
screenshots/logs-output.png

✅ Conclusion
This assignment successfully demonstrates:

AWS Lambda automation
EC2 lifecycle management
Debugging and issue resolution
CloudWatch monitoring


🔗 GitHub Repository
(Add your repo link here)

---

# ✅ ✅ 3. SMALL IMPROVEMENTS (HIGH IMPACT ⭐)

Do these quick upgrades:

---

## ✅ Add Comments in Code

```python
# Initialize EC2 client
ec2 = boto3.client('ec2')


