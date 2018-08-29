1. How long did you spend on this task?
    A: I spent roughly around 4 hours 30 minutes, on and off. Creating the python code and base CloudFormation template was simple. Since all my experience with Lambda functions and API Gateway are from AWS documentations, examples and AWS Solutions, it took me more time to research on the Custom DNS, Region specific API configuration and to come up with a design for the CI-CD pipeline.

    Python coding - 5 minutes
    CloudFormation Template - 1 hour
    Research with AWS Docs - 2+ hours
    Design for CI-CD, Backup and Security - 1+ hours

    '+' would denote extra 15 or 20 minutes

2. What would be the biggest improvement you'd make to submission if you had more time?
    A: There are number of improvements I would like to make in this give task
        1. Adding CI-CD pipeline using AWS resources like CodePipeline, CodeBuild and CodeDeploy
        2. Adding test cases to validate my CloudFormation template and the python code so that the output is a QA certified product
        3. Deploy the same with Terraform instead of CloudFormation. I chose CloudFormation because it was my strong area which I could really rely on my expertise.

3. What was the hardest thing about using terraform modules?
    A: I was not able to use Terraform for this task. My knowledge of Terraform modules is very limited. I have a theoretical knowledge of how Terraform works and very limited practical knowledge with only examples on how to create EC2 instances and required components like VPCs, Subnets, Security Groups for the EC2 Instance. I would like to learn more about it with real-time applications because there is nothing like on-job training. All my CloudFormation experience is from on-job training.

4. How did you secure your AWS Account Credentials?
    A: I always use IAM User to access my AWS Account, either through console or CLI. My policy is to follow Principle of Least Privilege (PoLP) when it comes to permissions to access and credentials. So for this task, I created an IAM user called `deloitte-test` with the policy permissions given below. I tried to follow the PoLP as much as possible, but there is always scope for improvement.

    ```
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudFormationPermissions",
            "Effect": "Allow",
            "Action": [
                "cloudformation:CreateUploadBucket",
                "cloudformation:CancelUpdateStack",
                "cloudformation:CreateStack",
                "cloudformation:DeleteStack",
                "cloudformation:UpdateStack",
                "cloudformation:UpdateTerminationProtection",
                "cloudformation:CreateChangeSet",
                "cloudformation:Describe*",
                "cloudformation:ContinueUpdateRollback",
                "cloudformation:EstimateTemplateCost",
                "cloudformation:PreviewStackUpdate",
                "cloudformation:List*",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:ValidateTemplate",
                "cloudformation:Get*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "LambdaPermissions",
            "Effect": "Allow",
            "Action": [
                "lambda:AddPermission",
                "lambda:InvokeFunction",
                "lambda:DeleteFunction",
                "lambda:PublishVersion",
                "lambda:List*",
                "lambda:CreateFunction",
                "lambda:Get*",
                "lambda:RemovePermission",
                "lambda:CreateAlias",
                "lambda:Update*",
                "apigateway:GET"
            ],
            "Resource": [
                "arn:aws:lambda:*:*:function:${project}*",
                "arn:aws:apigateway:*::/restapis"
            ]
        },
        {
            "Sid": "APIGatewayPermissions",
            "Effect": "Allow",
            "Action": "apigateway:*",
            "Resource": [
                "arn:aws:apigateway:*::/restapis/GATEWAY_ID/*",
                "arn:aws:apigateway:*::/restapis"
            ]
        },
        {
            "Sid": "CloudWatchLogsPermission",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:PutRetentionPolicy"
            ],
            "Resource": [
                "arn:aws:logs:*:*:log-group:*",
                "arn:aws:lambda:*:*:function:${project}*",
                "arn:aws:apigateway:*::/restapis/GATEWAY_ID/*",
                "arn:aws:apigateway:*::/restapis"
            ]
        },
        {
            "Sid": "CloudWatchLogStreamPermission",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams",
                "logs:GetLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:*:*:log-group:*:log-stream:*",
                "arn:aws:lambda:*:*:function:${project}*",
                "arn:aws:apigateway:*::/restapis/GATEWAY_ID/*",
                "arn:aws:apigateway:*::/restapis"
            ]
        },
        {
            "Effect": "Allow",
            "Sid": "GeneralPermissions",
            "Action": [
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:PutRolePolicy",
                "iam:DeleteRolePolicy",
                "iam:GetRole",
                "iam:PassRole",
                "iam:GetRole",
                "route53:Create*",
                "route53:Get*",
                "route53:List*",
                "route53:Update*",
                "route53:Change*",
                "s3:CreateBucket",
                "S3:Get*",
                "S3:List*",
                "S3:Put*",
                "S3:DeleteObject*"
            ],
            "Resource": "*"
        }
    ]
    }
    ```

    I also configured by laptop with the Access Key and Secret Key of the created user as separate profile in the <user-home>/.aws/credentials file as given below. Instead of using `aws configure` command, I create the files manually so that these keys are not saved as default

    ```
    [deloitte-test]
    aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
    aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ```

    So when I use the AWS CLI I have to add the options `--region us-east-1 --profile deloitte-test` with it so that I don't use my Administrator key or default access keys by accident.
