# update for cross account role

- need to create an IAM role in the central AWS account (Account A) 
- that the Lambda function will assume. 
- Then, create IAM roles in the target AWS accounts that trust the central account's role. 

## Steps to Deploy

1. Deploy the first CloudFormation template in the central account (Account A) to create the Lambda execution role.
2. Note the `LambdaExecutionRoleArn` from the output of the first template.
3. Deploy the second CloudFormation template in each target account, providing the central account ID and the `LambdaExecutionRoleArn` as parameters.

