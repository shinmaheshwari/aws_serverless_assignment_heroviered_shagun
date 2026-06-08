# AWS Serverless Assignment – Shagun Maheshwari

## 📌 Overview

This project demonstrates **AWS automation** using **Lambda and Boto3**. It includes multiple assignments focused on automating AWS infrastructure operations.

### Key Features:
- ✅ Automating EC2 instance management (Start/Stop)
- ✅ Restoring EC2 instances from snapshots
- ✅ Automatic backup of EC2 state before termination
- ✅ Managing security and monitoring
- ✅ Using CloudWatch for logging and debugging

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **AWS Lambda** | Serverless compute for automation |
| **Boto3** | AWS SDK for Python |
| **EC2** | Virtual machine instances |
| **EBS** | Block storage and snapshots |
| **S3** | Object storage for backups |
| **EventBridge** | Event-driven triggers |
| **IAM** | Access management and roles |
| **CloudWatch** | Logs and monitoring |

---

# ✅ Assignment 1: EC2 Auto Start/Stop

## 🎯 Objective

Automatically start and stop EC2 instances based on AWS tags using Lambda.

---

## 📋 Steps Followed

### 1. EC2 Setup

Created 2 EC2 instances with tags for automation:
- **Instance 1** → Tag: `Action = Auto-Stop`
- **Instance 2** → Tag: `Action = Auto-Start`

### 2. IAM Role Creation

**Role Name:** `lambda-ec2-management-role`

**Attached Policies:**
- `AmazonEC2FullAccess` - Full EC2 permissions
- `AWSLambdaBasicExecutionRole` - CloudWatch logging

### 3. Lambda Function Setup

| Configuration | Value |
|--------------|-------|
| **Function Name** | `ec2-auto-start-stop` |
| **Runtime** | Python 3.x |
| **Timeout** | 15 seconds |
| **Memory** | 128 MB |
| **Execution Role** | `lambda-ec2-management-role` |

### 4. Lambda Code Implementation

```python
import boto3

def lambda_handler(event, context):
    """
    Lambda function to automatically start and stop EC2 instances based on tags.
    
    - Finds instances tagged with 'Action: Auto-Stop' and stops running ones
    - Finds instances tagged with 'Action: Auto-Start' and starts stopped ones
    """
    
    print("Lambda execution started")
    
    # Initialize EC2 client
    ec2 = boto3.client('ec2')
    
    # ===== STOP INSTANCES SECTION =====
    # Find instances with Auto-Stop tag that are currently running
    stop_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    # Extract instance IDs from response
    stop_ids = [i['InstanceId'] for r in stop_instances['Reservations'] for i in r['Instances']]
    print("Auto-Stop Found:", stop_ids)
    
    # Stop instances if any found
    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print("Stopped:", stop_ids)
    
    # ===== START INSTANCES SECTION =====
    # Find instances with Auto-Start tag that are currently stopped
    start_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )
    
    # Extract instance IDs from response
    start_ids = [i['InstanceId'] for r in start_instances['Reservations'] for i in r['Instances']]
    print("Auto-Start Found:", start_ids)
    
    # Start instances if any found
    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print("Started:", start_ids)
    
    print("Execution complete")
    return {
        'statusCode': 200,
        'body': f'Stopped: {stop_ids}, Started: {start_ids}'
    }
```

---

## 🧪 Testing & Validation

### Test Execution
- ✅ Manually triggered Lambda using test event `{}`
- ✅ Verified EC2 instance states changed as expected
- ✅ Confirmed CloudWatch logs captured all operations

### ✅ Output Results
| Action | Status | Verification |
|--------|--------|--------------|
| Instances with **Auto-Stop** | Stopped ✓ | EC2 Dashboard |
| Instances with **Auto-Start** | Started ✓ | EC2 Dashboard |
| Logs Generated | Captured ✓ | CloudWatch Logs |

---

## ⚠️ Issues Faced & Fixes

### Issue 1: Lambda Timeout Error
**Error Message:**
```
Task timed out after 3.01 seconds
```

**Root Cause:** Default timeout was too short for EC2 API calls

**Fix Applied:**
- Increased Lambda timeout to **15 seconds** in function configuration

---

### Issue 2: Missing CloudWatch Logs
**Problem:** No execution logs were visible

**Root Cause:** Lambda didn't have CloudWatch permissions

**Fix Applied:**
- Added `AWSLambdaBasicExecutionRole` policy to IAM role

---

### Issue 3: No Output in Logs
**Problem:** Function executed but didn't show expected output

**Root Cause:** Instances were already in the target state

**Fix Applied:**
- Changed instance states manually
- Added detailed `print()` statements for debugging

---

## 📸 Screenshots
- `screenshots/ec2-before.png` - EC2 instances before execution
- `screenshots/ec2-after.png` - EC2 instances after execution
- `screenshots/lambda-config.png` - Lambda function configuration
- `screenshots/logs-output.png` - CloudWatch logs with execution details

---

## ✅ Assignment 1 Conclusion

This assignment successfully demonstrates:
- ✓ AWS Lambda automation
- ✓ EC2 lifecycle management using tags
- ✓ Debugging and issue resolution
- ✓ CloudWatch monitoring and logging

---

---

# ✅ Assignment 17: Restore EC2 Instance from Snapshot

## 🎯 Objective

Automate EC2 disaster recovery by creating a Lambda function that:
- Fetches the latest snapshot of a running EC2 instance
- Creates a new EBS volume from the snapshot
- Launches a new EC2 instance automatically

---

## 📋 AWS Services Used

- **AWS Lambda** - Serverless automation
- **Amazon EC2** - Virtual machine instances
- **Amazon EBS** - Block storage and snapshots
- **AWS IAM** - Access control and roles
- **Amazon CloudWatch** - Execution logs

---

## 🏗️ Architecture Flow

```
┌─────────────────────────────────────────────────┐
│       Lambda Function Triggered                 │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Fetch Running EC2 Instance Details             │
│  (InstanceId, AMI, AvailabilityZone)            │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Retrieve Latest Snapshot from Volume           │
│  (Sort by StartTime)                            │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Create New EBS Volume from Snapshot            │
│  (Type: gp2, Same AvailabilityZone)             │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Launch New EC2 Instance                        │
│  (Same AMI, Same InstanceType)                  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Store Execution Logs in CloudWatch             │
│  (Success confirmation)                         │
└─────────────────────────────────────────────────┘
```

---

## 📋 Steps Followed

### Step 1: Create IAM Role for Lambda

1. Navigate to **IAM → Roles → Create Role**
2. Select **AWS Service** → **Lambda**
3. Attach Policies:
   - `AmazonEC2FullAccess`
   - `AWSLambdaBasicExecutionRole`
4. Role Name: `LambdaEC2RestoreRole`
5. Click **Create Role**

---

### Step 2: Create Lambda Function

1. Open **AWS Lambda Console**
2. Click **Create Function**
3. Choose **Author from scratch**
4. Configure:
   - **Function Name:** `EC2SnapshotRestore`
   - **Runtime:** Python 3.x
   - **Execution Role:** `LambdaEC2RestoreRole`
5. Click **Create Function**

---

### Step 3: Add Lambda Python Code

```python
import boto3

# Initialize EC2 client for AWS API calls
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Lambda function to restore EC2 instance from latest snapshot.
    
    Steps:
    1. Fetch the first running EC2 instance
    2. Get its root volume ID
    3. Find the latest snapshot of that volume
    4. Create a new EBS volume from the snapshot
    5. Launch a new EC2 instance with the same configuration
    """
    
    try:
        # ===== STEP 1: Fetch Running EC2 Instance =====
        # Get all running instances and select the first one
        response = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )
        
        # Extract first running instance
        instance = response['Reservations'][0]['Instances'][0]
        
        instance_id = instance['InstanceId']
        ami_id = instance['ImageId']
        instance_type = instance['InstanceType']
        availability_zone = instance['Placement']['AvailabilityZone']
        
        print(f"Source Instance ID: {instance_id}")
        print(f"Instance Type: {instance_type}")
        print(f"AMI ID: {ami_id}")
        print(f"Availability Zone: {availability_zone}")
        
        # ===== STEP 2: Get Root Volume ID =====
        # Find the EBS volume attached to the instance
        volume_id = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']
        print(f"Volume ID: {volume_id}")
        
        # ===== STEP 3: Fetch Latest Snapshot =====
        # Get all snapshots for this volume
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
        
        # Sort snapshots by StartTime (latest first)
        snapshot_list.sort(
            key=lambda x: x['StartTime'],
            reverse=True
        )
        
        latest_snapshot = snapshot_list[0]
        snapshot_id = latest_snapshot['SnapshotId']
        
        print(f"Latest Snapshot ID: {snapshot_id}")
        print(f"Snapshot State: {latest_snapshot['State']}")
        
        # ===== STEP 4: Create New EBS Volume =====
        # Create volume from latest snapshot
        new_volume = ec2.create_volume(
            SnapshotId=snapshot_id,
            AvailabilityZone=availability_zone,
            VolumeType='gp2'
        )
        
        new_volume_id = new_volume['VolumeId']
        print(f"New Volume Created: {new_volume_id}")
        
        # ===== STEP 5: Launch New EC2 Instance =====
        # Launch new instance with same configuration
        new_instance = ec2.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            Placement={
                'AvailabilityZone': availability_zone
            }
        )
        
        new_instance_id = new_instance['Instances'][0]['InstanceId']
        print(f"New EC2 Instance Created: {new_instance_id}")
        
        # Return success response
        return {
            'statusCode': 200,
            'body': {
                'message': 'EC2 restoration successful',
                'new_instance_id': new_instance_id,
                'new_volume_id': new_volume_id,
                'snapshot_id': snapshot_id
            }
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
```

---

### Step 4: Test Lambda Function

1. Click **Test** button
2. Create test event: `{}`
3. Click **Invoke/Test**
4. Verify successful execution and response

---

### Step 5: Verify New EBS Volume

1. Open **EC2 Console**
2. Navigate to **Elastic Block Store → Volumes**
3. Verify the newly created volume is present with status `available`

---

### Step 6: Verify Restored EC2 Instance

1. Navigate to **EC2 → Instances**
2. Verify the newly launched instance is running
3. Check that instance type and availability zone match the source instance

---

### Step 7: Verify CloudWatch Logs

1. Open **CloudWatch**
2. Navigate to **Log Groups**
3. Open `/aws/lambda/EC2SnapshotRestore`
4. Verify execution logs showing:
   - Source instance details
   - Latest snapshot ID
   - New volume creation confirmation
   - New EC2 instance creation confirmation

**Example Log Output:**
```
Source Instance ID: i-0123456789abcdef0
Instance Type: t3.micro
AMI ID: ami-xxxxxxxx
Availability Zone: ap-south-1a
Volume ID: vol-0987654321fedcba0
Latest Snapshot ID: snap-xxxxxxxx
Snapshot State: completed
New Volume Created: vol-1111111111111111
New EC2 Instance Created: i-2222222222222222
```

---

## ✅ Assignment 17 Conclusion

This assignment successfully demonstrates:
- ✓ Automated EC2 disaster recovery
- ✓ Snapshot retrieval and management
- ✓ EBS volume creation from snapshots
- ✓ EC2 instance restoration
- ✓ CloudWatch logging for monitoring

---

---

# ✅ Assignment 18: Autosave EC2 Instance State Before Shutdown

## 🎯 Objective

Automatically save EC2 instance information into an S3 bucket before the instance is terminated using EventBridge and Lambda.

---

## 📋 AWS Services Used

- **Amazon EC2** - Virtual machine instances
- **AWS Lambda** - Serverless automation
- **Amazon S3** - Object storage for backups
- **Amazon EventBridge** - Event-driven triggers
- **AWS IAM** - Access control
- **Amazon CloudWatch** - Execution logs

---

## 🏗️ Architecture Flow

```
┌──────────────────────────────────────────────────────┐
│      EC2 Instance Termination Event                  │
│      (User initiates instance termination)           │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  EventBridge Detects State-Change Notification       │
│  (Catches 'terminated' state)                        │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Triggers Lambda Function                            │
│  (EC2StateBackup Lambda)                             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Lambda Fetches Instance Details from Event          │
│  (instance-id from EventBridge payload)              │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Extract Instance Information                        │
│  (Type, AMI, LaunchTime, AvailabilityZone, State)    │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Create JSON Backup File                             │
│  (instance-id-timestamp.json)                        │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Upload to S3 Bucket                                 │
│  (ec2-backup-assignment18)                           │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Store Execution Logs in CloudWatch                  │
│  (Success confirmation with file details)            │
└──────────────────────────────────────────────────────┘
```

---

## 📋 Steps Followed

### Step 1: Create S3 Bucket for Backups

1. Open **S3 Console**
2. Click **Create Bucket**
3. Enter Bucket Name: `ec2-backup-assignment18`
4. Keep default settings
5. Click **Create Bucket**

---

### Step 2: Create IAM Role for Lambda

1. Navigate to **IAM → Roles → Create Role**
2. Select **AWS Service** → **Lambda**
3. Attach Policies:
   - `AmazonEC2ReadOnlyAccess` - Read EC2 instance details
   - `AmazonS3FullAccess` - Write backups to S3
   - `AWSLambdaBasicExecutionRole` - CloudWatch logging
4. Role Name: `LambdaEC2BackupRole`
5. Click **Create Role**

---

### Step 3: Create Lambda Function

1. Open **AWS Lambda Console**
2. Click **Create Function**
3. Choose **Author from scratch**
4. Configure:
   - **Function Name:** `EC2StateBackup`
   - **Runtime:** Python 3.x
   - **Execution Role:** `LambdaEC2BackupRole`
5. Click **Create Function**

---

### Step 4: Add Lambda Python Code

```python
import boto3
import json
from datetime import datetime

# Initialize EC2 and S3 clients
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

# S3 bucket name for storing backups
BUCKET_NAME = 'ec2-backup-assignment18'

def lambda_handler(event, context):
    """
    Lambda function to backup EC2 instance state before termination.
    
    Triggered by EventBridge when EC2 instance is terminated.
    Captures instance details and saves them as JSON to S3.
    
    Expected EventBridge event format:
    {
        "detail": {
            "instance-id": "i-xxxxxxxx",
            "state": "terminated"
        }
    }
    """
    
    try:
        # ===== STEP 1: Extract Instance ID from Event =====
        # Get instance ID from EventBridge event
        instance_id = event['detail']['instance-id']
        
        print(f"Instance Terminated: {instance_id}")
        print("Starting backup process...")
        
        # ===== STEP 2: Fetch EC2 Instance Details =====
        # Use EC2 API to get detailed instance information
        response = ec2.describe_instances(
            InstanceIds=[instance_id]
        )
        
        instance = response['Reservations'][0]['Instances'][0]
        
        # ===== STEP 3: Extract Backup Data =====
        # Create dictionary with key instance information
        instance_data = {
            'InstanceId': instance.get('InstanceId'),
            'InstanceType': instance.get('InstanceType'),
            'AMI_ID': instance.get('ImageId'),
            'LaunchTime': str(instance.get('LaunchTime')),
            'State': instance.get('State')['Name'],
            'AvailabilityZone': instance['Placement']['AvailabilityZone'],
            'BackupTimestamp': datetime.now().isoformat()
        }
        
        print(f"Instance Data Captured:")
        print(f"  - Type: {instance_data['InstanceType']}")
        print(f"  - AMI: {instance_data['AMI_ID']}")
        print(f"  - Zone: {instance_data['AvailabilityZone']}")
        
        # ===== STEP 4: Convert to JSON Format =====
        # Convert dictionary to JSON string with formatting
        json_data = json.dumps(instance_data, indent=4)
        
        # ===== STEP 5: Generate Backup Filename =====
        # Create filename with instance ID and timestamp
        file_name = f"{instance_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        
        print(f"Uploading backup file: {file_name}")
        
        # ===== STEP 6: Upload Backup to S3 =====
        # Put the JSON data into S3 bucket
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json_data,
            ContentType='application/json'
        )
        
        print(f"✓ Backup saved to S3: s3://{BUCKET_NAME}/{file_name}")
        
        # Return success response
        return {
            'statusCode': 200,
            'body': {
                'message': f'Successfully backed up {instance_id}',
                'file_location': f's3://{BUCKET_NAME}/{file_name}',
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"✗ Error during backup: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
```

---

### Important Configuration Note

Make sure the `BUCKET_NAME` variable matches your S3 bucket name:

```python
BUCKET_NAME = 'ec2-backup-assignment18'  # Replace with your bucket name
```

---

### Step 5: Deploy Lambda Function

1. Click **Deploy** button to save the function

---

### Step 6: Create EventBridge Rule

1. Open **Amazon EventBridge**
2. Navigate to **Rules → Create Rule**
3. Select **Advanced Builder**
4. Configure Rule:
   - **Rule Name:** `EC2TerminationTrigger`
5. Configure Event Pattern:
   ```json
   {
     "source": ["aws.ec2"],
     "detail-type": ["EC2 Instance State-change Notification"],
     "detail": {
       "state": ["terminated"]
     }
   }
   ```
6. Configure Target:
   - **Target Type:** AWS Service
   - **Target:** Lambda Function
   - **Function:** `EC2StateBackup`
7. Click **Create Rule**

---

### Step 7: Test - Terminate an EC2 Instance

1. Open **EC2 → Instances**
2. Select a test EC2 instance
3. Click **Instance State → Terminate Instance**
4. Confirm termination

---

### Step 8: Verify Backup File in S3

1. Open **S3 → ec2-backup-assignment18**
2. Verify the JSON backup file is present
3. File naming format: `i-xxxxxxxx-20260608120000.json`
4. Click on file to view its contents

**Example JSON Backup File:**
```json
{
    "InstanceId": "i-0123456789abcdef0",
    "InstanceType": "t3.micro",
    "AMI_ID": "ami-xxxxxxxx",
    "LaunchTime": "2026-06-08 10:00:00+00:00",
    "State": "terminated",
    "AvailabilityZone": "ap-south-1a",
    "BackupTimestamp": "2026-06-08T12:30:45.123456"
}
```

---

### Step 9: Verify CloudWatch Logs

1. Open **CloudWatch**
2. Navigate to **Log Groups**
3. Open `/aws/lambda/EC2StateBackup`
4. Verify execution logs showing:
   - Instance terminated event
   - Instance data captured
   - S3 backup file uploaded
   - Success confirmation

**Example Log Output:**
```
Instance Terminated: i-0123456789abcdef0
Starting backup process...
Instance Data Captured:
  - Type: t3.micro
  - AMI: ami-xxxxxxxx
  - Zone: ap-south-1a
Uploading backup file: i-0123456789abcdef0-20260608120000.json
✓ Backup saved to S3: s3://ec2-backup-assignment18/i-0123456789abcdef0-20260608120000.json
```

---

## ✅ Final Output

When an EC2 instance is terminated:
1. ✓ EventBridge immediately detects the termination event
2. ✓ Lambda function automatically executes
3. ✓ EC2 instance data is extracted and formatted as JSON
4. ✓ Backup file is uploaded to S3 with timestamp
5. ✓ Execution logs are generated in CloudWatch
6. ✓ Instance information is preserved for auditing and recovery

---

## ✅ Assignment 18 Conclusion

This assignment successfully demonstrates:
- ✓ Event-driven automation using EventBridge
- ✓ Automatic EC2 state backup on termination
- ✓ S3 integration for backup storage
- ✓ JSON data serialization
- ✓ CloudWatch logging and monitoring
- ✓ Infrastructure auditing and compliance

---

---

# ⭐ Summary of All Assignments

| Assignment | Objective | Key AWS Services | Status |
|-----------|-----------|------------------|--------|
| **1** | EC2 Auto Start/Stop | Lambda, EC2, IAM | ✅ Complete |
| **17** | Restore from Snapshot | Lambda, EC2, EBS, IAM | ✅ Complete |
| **18** | Auto-Backup EC2 State | Lambda, EC2, S3, EventBridge, IAM | ✅ Complete |

---

## 🎓 Learning Outcomes

Through these assignments, you have learned:

1. **AWS Lambda Fundamentals**
   - Creating and configuring Lambda functions
   - Setting appropriate timeouts and memory
   - Understanding execution roles and permissions

2. **AWS EC2 Management**
   - Tagging instances for automation
   - Starting/stopping instances via API
   - Instance lifecycle management
   - Retrieving instance metadata

3. **AWS IAM Security**
   - Creating least-privilege IAM roles
   - Attaching appropriate policies
   - Understanding EC2, S3, and Lambda permissions

4. **Data Management**
   - EBS snapshots and volumes
   - S3 bucket operations
   - JSON data serialization
   - CloudWatch logging

5. **Event-Driven Architecture**
   - EventBridge rules and triggers
   - Lambda event handling
   - Automation workflows

6. **Debugging & Monitoring**
   - Using CloudWatch Logs
   - Identifying and fixing timeout errors
   - Print statements for debugging
   - Monitoring execution results

---

## 📚 Best Practices Applied

✓ **Code Comments** - All functions include detailed comments explaining functionality
✓ **Error Handling** - Try-catch blocks for graceful error management
✓ **Logging** - Comprehensive print statements for CloudWatch logging
✓ **Security** - IAM roles with specific permissions (not overly permissive)
✓ **Configuration** - Timeout settings appropriate for API calls
✓ **Documentation** - Complete step-by-step guides for reproduction

---

## 🔗 Repository Links

- **Repository:** [aws_serverless_assignment_heroviered_shagun](https://github.com/shinmaheshwari/aws_serverless_assignment_heroviered_shagun)
- **Branch:** main
- **Author:** Shagun Maheshwari

---

## 📝 Notes

- All Lambda functions are Python 3.x compatible
- CloudWatch logs are essential for debugging
- EventBridge rules enable event-driven automation
- S3 backups provide disaster recovery capabilities
- Proper IAM roles prevent security issues

---

**Last Updated:** June 8, 2026  
**Status:** ✅ All Assignments Complete
