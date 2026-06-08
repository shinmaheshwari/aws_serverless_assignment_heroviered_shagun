# AWS Serverless Assignment Collection

A comprehensive collection of AWS serverless automation projects demonstrating Lambda, EventBridge, Boto3, and AWS infrastructure automation.

---

## 📋 Table of Contents

1. [Assignment 5: Auto-Tagging EC2 Instances](#assignment-5-auto-tagging-ec2-instances)
2. [Assignment 17: Restore EC2 Instance from Snapshot](#assignment-17-restore-ec2-instance-from-snapshot)
3. [Assignment 18: Autosave EC2 Instance State](#assignment-18-autosave-ec2-instance-state)
4. [Assignment 19: Load Balancer Health Check](#assignment-19-load-balancer-health-check)

---

## Assignment 5: Auto-Tagging EC2 Instances

### Objective

Automate the tagging of newly launched EC2 instances using AWS Lambda and Boto3. Whenever a new EC2 instance enters the running state, AWS EventBridge triggers a Lambda function that automatically applies predefined tags.

### AWS Services Used

- Amazon EC2
- AWS Lambda
- AWS IAM
- Amazon EventBridge
- Amazon CloudWatch Logs
- Boto3

### Architecture Flow

```
EC2 Instance Launch
        ↓
EventBridge Detects EC2 Running State
        ↓
Triggers AWS Lambda Function
        ↓
Lambda Uses Boto3 to Add Tags
        ↓
Tags Applied to EC2 Instance
```

### Implementation Steps

1. **Create IAM Role for Lambda**
   - Role Name: `LambdaEC2AutoTagRole`
   - Policies: `AmazonEC2FullAccess`, `AWSLambdaBasicExecutionRole`

2. **Create Lambda Function**
   - Function Name: `EC2AutoTagger`
   - Runtime: Python 3.x
   - Code Reference: [`assignment5-auto-tagging-ec2/lambda_function.py`](assignment5-auto-tagging-ec2/lambda_function.py)

3. **Create EventBridge Rule**
   - Rule Name: `EC2LaunchTrigger`
   - Event Pattern: EC2 Instance State-change Notification (running state)
   - Target: Lambda Function `EC2AutoTagger`

4. **Test the Automation**
   - Launch a new EC2 instance
   - Verify tags are automatically applied
   - Check CloudWatch logs for confirmation

### Expected Output

| Key | Value |
|------|------|
| LaunchDate | Current Date |
| Environment | Development |

### Documentation

For detailed step-by-step instructions, screenshots, and implementation details, refer to: [`assignment5-auto-tagging-ec2/README.md`](assignment5-auto-tagging-ec2/README.md)

> **📸 Note**: Screenshots for this assignment are located in [`assignment5-auto-tagging-ec2/screenshots/`](assignment5-auto-tagging-ec2/screenshots/)

---

## Assignment 17: Restore EC2 Instance from Snapshot

### Objective

Automate the EC2 recovery process using AWS Lambda and Boto3. The Lambda function fetches the latest snapshot of an EC2 instance, creates a new EBS volume from the snapshot, and launches a new EC2 instance automatically.

### AWS Services Used

- AWS Lambda
- Amazon EC2
- Amazon EBS Snapshots
- AWS IAM
- Amazon CloudWatch
- Boto3

### Architecture Flow

```
Lambda Function Triggered
        ↓
Fetch Running EC2 Instance Details
        ↓
Retrieve Latest Snapshot
        ↓
Create New EBS Volume
        ↓
Launch New EC2 Instance
        ↓
Store Logs in CloudWatch
```

### Implementation Steps

1. **Create IAM Role for Lambda**
   - Role Name: `LambdaEC2RestoreRole`
   - Policies: `AmazonEC2FullAccess`, `AWSLambdaBasicExecutionRole`

2. **Create Lambda Function**
   - Function Name: `EC2SnapshotRestore`
   - Runtime: Python 3.x
   - Code Reference: [`assignment17-ec2-restore-from-snapshot/lambda-function.py`](assignment17-ec2-restore-from-snapshot/lambda-function.py)

3. **Lambda Function Capabilities**
   - Fetches running EC2 instance details
   - Retrieves volume information
   - Sorts and selects latest snapshot
   - Creates new EBS volume from snapshot
   - Launches new EC2 instance in same availability zone

4. **Test Lambda Function**
   - Create test event
   - Invoke Lambda function
   - Monitor execution logs

5. **Verify Output**
   - Check EC2 Instances for newly created instance
   - Verify EBS Volumes for new volume
   - Review CloudWatch logs for detailed execution information

### Expected CloudWatch Log Output

```
Source Instance ID: i-xxxxxxxx
Latest Snapshot ID: snap-xxxxxxxx
New Volume Created: vol-xxxxxxxx
New EC2 Instance Created: i-yyyyyyyy
```

### Documentation

For detailed step-by-step instructions, screenshots, and implementation details, refer to: [`assignment17-ec2-restore-from-snapshot/README.md`](assignment17-ec2-restore-from-snapshot/README.md)

> **📸 Note**: Screenshots for this assignment are located in [`assignment17-ec2-restore-from-snapshot/screenshots/`](assignment17-ec2-restore-from-snapshot/screenshots/)

---

## Assignment 18: Autosave EC2 Instance State

### Objective

Automatically save EC2 instance information into an S3 bucket before the instance is terminated. Using AWS Lambda, Boto3, and EventBridge, EC2 termination events are detected, instance details are fetched, and backup data is stored in S3.

### AWS Services Used

- Amazon EC2
- AWS Lambda
- Amazon S3
- Amazon EventBridge
- AWS IAM
- Amazon CloudWatch
- Boto3

### Architecture Flow

```
EC2 Instance Termination
            ↓
EventBridge Detects Termination Event
            ↓
Triggers Lambda Function
            ↓
Lambda Fetches Instance Details
            ↓
Save Backup File to S3 Bucket
            ↓
CloudWatch Logs Generated
```

### Implementation Steps

1. **Create S3 Bucket**
   - Bucket Name: `ec2-backup-assignment18`
   - Default settings

2. **Create IAM Role for Lambda**
   - Role Name: `LambdaEC2BackupRole`
   - Policies: `AmazonEC2ReadOnlyAccess`, `AmazonS3FullAccess`, `AWSLambdaBasicExecutionRole`

3. **Create Lambda Function**
   - Function Name: `EC2StateBackup`
   - Runtime: Python 3.x
   - Code Reference: [`assignment18-autoSave-ec2-state/lambda-function.py`](assignment18-autoSave-ec2-state/lambda-function.py)

4. **Create EventBridge Rule**
   - Rule Name: `EC2TerminationTrigger`
   - Event Pattern: EC2 Instance State-change Notification (terminated state)
   - Target: Lambda Function `EC2StateBackup`

5. **Test the Automation**
   - Terminate an EC2 instance
   - Verify backup JSON file in S3 bucket
   - Check CloudWatch logs for execution details

### Expected JSON Backup File

```json
{
    "InstanceId": "i-0123456789abcdef0",
    "InstanceType": "t3.micro",
    "AMI_ID": "ami-xxxxxxxx",
    "LaunchTime": "2026-06-08 10:00:00+00:00",
    "State": "terminated",
    "AvailabilityZone": "ap-south-1a"
}
```

### Documentation

For detailed step-by-step instructions, screenshots, and implementation details, refer to: [`assignment18-autoSave-ec2-state/README.md`](assignment18-autoSave-ec2-state/README.md)

> **📸 Note**: Screenshots for this assignment are located in [`assignment18-autoSave-ec2-state/screenshots/`](assignment18-autoSave-ec2-state/screenshots/)

---

## Assignment 19: Load Balancer Health Check

### Objective

Implement automated health checks for load-balanced EC2 instances using AWS Lambda and Boto3. Monitor application health and automatically manage instance states based on health check results.

### AWS Services Used

- Amazon EC2
- AWS Lambda
- Elastic Load Balancing (ELB/ALB)
- AWS IAM
- Amazon CloudWatch
- Boto3

### Implementation Steps

1. **Create IAM Role for Lambda**
   - Attach appropriate EC2 and Load Balancing permissions

2. **Create Lambda Function**
   - Function Name: Appropriate to your health check requirements
   - Runtime: Python 3.x
   - Code Reference: [`assignment19-LB-Health-check/lambda-function.py`](assignment19-LB-Health-check/lambda-function.py)

3. **Configure Health Checks**
   - Set up health check endpoints
   - Configure health check intervals
   - Define failure thresholds

4. **Monitor Results**
   - Review CloudWatch metrics
   - Monitor Lambda execution logs
   - Track instance health status

### Documentation

For detailed step-by-step instructions and implementation details, refer to: [`assignment19-LB-Health-check/README.md`](assignment19-LB-Health-check/README.md)

> **📸 Note**: Screenshots for this assignment are located in [`assignment19-LB-Health-check/screenshots/`](assignment19-LB-Health-check/screenshots/)

---

## 🛠️ Technologies & Tools

- **AWS Services**: Lambda, EC2, S3, EventBridge, IAM, CloudWatch, ELB
- **Programming Language**: Python 3.x
- **Libraries**: Boto3 (AWS SDK for Python)
- **Automation**: AWS Lambda, EventBridge, CloudWatch

---

## 📁 Repository Structure

```
aws_serverless_assignment_heroviered_shagun/
│
├── README.md (this file)
│
├── assignment5-auto-tagging-ec2/
│   ├── README.md
│   ├── lambda_function.py
│   └── screenshots/
│
├── assignment17-ec2-restore-from-snapshot/
│   ├── README.md
│   ├── lambda-function.py
│   └── screenshots/
│
├── assignment18-autoSave-ec2-state/
│   ├── README.md
│   ├── lambda-function.py
│   └── screenshots/
│
└── assignment19-LB-Health-check/
    ├── README.md
    ├── lambda-function.py
    └── screenshots/
```

---

## 🚀 Key Features

### Assignment 5: EC2 Auto-Tagging
- ✅ Automatic tag application on EC2 launch
- ✅ EventBridge-triggered Lambda execution
- ✅ Custom tag values with current date
- ✅ CloudWatch logging for audit trail

### Assignment 17: EC2 Snapshot Restore
- ✅ Automated snapshot retrieval
- ✅ EBS volume creation from snapshot
- ✅ EC2 instance launch from AMI
- ✅ Disaster recovery automation

### Assignment 18: EC2 State Backup
- ✅ Automatic state backup before termination
- ✅ JSON backup file generation
- ✅ S3 storage for long-term retention
- ✅ Complete audit trail in CloudWatch

### Assignment 19: Load Balancer Health Check
- ✅ Automated health monitoring
- ✅ Instance state management
- ✅ Health check orchestration
- ✅ CloudWatch integration

---

## 📝 Common Workflow

1. **Setup Phase**
   - Create required AWS resources (IAM roles, S3 buckets, etc.)
   - Deploy Lambda functions with provided code

2. **Configuration Phase**
   - Create EventBridge rules for event detection
   - Link Lambda functions as targets

3. **Testing Phase**
   - Trigger events manually or automatically
   - Monitor CloudWatch logs
   - Verify expected outcomes

4. **Monitoring Phase**
   - Review CloudWatch metrics
   - Check application logs
   - Monitor cost implications

---

## 🔐 Security Considerations

- Use IAM roles with least privilege principle
- Enable CloudWatch logging for audit trails
- Store sensitive configuration in environment variables
- Review Lambda execution permissions regularly
- Monitor CloudWatch logs for unusual activity

---

## 📚 References

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Amazon EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Amazon EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/)
- [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/)

---

## 📧 Contact & Support

For questions or issues regarding these assignments, refer to the individual assignment READMEs for detailed troubleshooting steps and implementation guidance.

---

**Last Updated**: June 8, 2026
**Language**: Python 3.x
**AWS Region**: Multi-region compatible
