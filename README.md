# Deploy a Lambda Function to Stop Long-Running EC2 Instances

## cloudformation-template.yaml

### Explanation

1. **LambdaExecutionRole**: Defines an IAM role with the necessary permissions for the Lambda function.
   - Allows the Lambda function to assume the role.
   - Grants permissions to describe and stop EC2 instances, publish SNS messages, get caller identity, and describe the AWS account.

2. **StopLongRunningEC2InstancesFunction**: Defines the Lambda function.
   - Specifies the handler, role, code location (S3 bucket and key), runtime, and timeout.
   - Sets an environment variable for the SNS topic ARN.

3. **Outputs**: Provides the ARN of the deployed Lambda function as an output.

### Steps to Deploy

1. Package your Lambda function code and upload it to an S3 bucket.
2. Replace `your-s3-bucket-name` and `your-s3-key` with the actual S3 bucket name and key where your Lambda function code is stored.
3. Replace `arn:aws:sns:region:account-id:topic-name` with your actual SNS topic ARN.
4. Save the CloudFormation template to a file (e.g., `cloudformation-template.yaml`).
5. Deploy the CloudFormation stack using the AWS CLI:

```sh
aws cloudformation create-stack --stack-name StopLongRunningEC2InstancesStack --template-body file://cloudformation-template.yaml --capabilities CAPABILITY_NAMED_IAM
```

