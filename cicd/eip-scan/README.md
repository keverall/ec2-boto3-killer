# Steps to Deploy

- Deploy Central Account Role:

- Deploy central-account.yaml in the central account.
  
- Note the LambdaExecutionRoleArn from the output.
  
- Deploy Target Account Role:

- Deploy target-account.yaml in each target account
  
- providing the central account ID and LambdaExecutionRoleArn as parameters.
  
- Deploy Lambda Function:

- Deploy lambda-deployment.yaml in the central account
- providing the LambdaExecutionRoleArn as a parameter
- Ensure the Lambda code is uploaded to the specified S3 bucket
- Example Deployment Commands
- This setup ensures that your Lambda function can assume roles in the target accounts 
- and perform the necessary EC2 actions, 
- while also sending SNS alerts for the actions taken.
