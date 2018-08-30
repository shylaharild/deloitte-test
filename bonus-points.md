## 1. Instructions to Setup Vanilla AWS Account & generate credentials to execute Terraform/CloudFormation code.

The following are the steps to create a vanilla AWS Account
  1. Open your favourite browser, go to `aws.amazon.com` and Click on the `Sign In to the Console` button on the top right corner
  2. Once done, click on the `Create a new AWS Account` button
  3. Fill in the details like Email address, password, confirm password and AWS account name. Click `Continue`
  4. Fill in the contact details by choosing the desired Account Type. Click `Create Account and Continue`
  5. Enter the Payment Information details and billing address information. Click on `Secure Submit`.
  6. Provide the valid mobile phone number for the Phone Verification. Click on `Call Me Now`. Make sure you have the phone with you as you will receive a call from Amazon to verify if you're a genuine person. Enter the 4 digit number displayed on your browser when asked during the call using the mobile phone keypad. Click `Continue`
  7. In the next page, select the desired support plan for the AWS account. I choose Basic Plan which is `Free`
  8. Voila. You're good to go. Click on `Sign In to the Console`. This will take you back to the first page

Sign in using the email address that you used to sign up to access your AWS Account. It is called the root credential. Next step is to create an IAM User as it is not a best practice to use the root credentials. Those credentials must be printed out in a paper, sealed in an envelope and locked in a safe box.

To create an Administrator IAM User, follow the steps given below.
  1. Login using root credentials only for this time
  2. Click on the `Services` button on the top left side & navigate to `IAM` service
  3. In the IAM Dashboard, you can find the security status section. Do all the 5 to secure your account
  4. Click on the `Users` in the left tab
  5. Provide the username, access type, & password and click `Next: Permissions`
  6. Click on `Attach existing policies directly`. In the next page, search for `Administrator Access` in the policies, select it and click `Next: Review`
  7. Review the given user details and click `Create User`
  8. Keep the generated Access Key and Secret Key safe

To create the user to execute the code, do the following.

  1. Navigate to IAM Service Dashboard after logging in as Administrator IAM User
  2. Click on the `Policies` link on the left tab
  3. Click on create policy and navigate to `JSON` tab
  4. Copy paste the policy given below in the editor and click on `Review Policy`
  5. Give a name to the policy and hit `Create Policy`
  6. Now follow the same steps to create the IAM user `deloitte-test`
  7. While selecting the policy, search for the newly created policy and do the rest of the steps to create the user

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
            "iam:Get*",
            "iam:PassRole",
            "iam:ChangePassword"
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

## 2. A proposed solution for Continuous Integration, including where the agents would live

My design for the Continuous Integration is to use AWS service called CodeBuild. We can use this along with another AWS service called CodePipeline. The CodePipeline will connect the SCM, in our case Github using the git hook and GithubOAuth Credentials, and will poll the repository for changes at regular intervals. When the change is found, it will pull the codebase and then trigger the AWS CodeBuild which will build & archive the code as per the given instruction and configuration in the `build.yaml` file and finally transfer the archive into the S3 bucket for it to be deployed into the lambda function.

AWS CodeBuild required `build.yaml` to be present on the root of the repository. The example of the `build.yaml` file is given below. To configure the CodeBuild Build Project, you need to specify the following

* Github repository url in the `Current Source`
* Base Image for CodeBuild to create an instance and perform the build
* Service Role where it has required IAM Permissions
* Optional: VPC in which the CodeBuild will create the instance for build process

Jenkins can also be used as a Continuous Integration tool with the AWS CodePipeline.

As a part of Continuous Deployment, AWS CodeDeploy can be used with AWS CodePipeline to deploy the new version of the application to the AWS Lambda. Thus creating a full CI-CD pipeline so that every check-in to the SCM is taken to the environment through a fully automated deployment process.

```bash
build.yaml

version: 0.2

phases:
  install:
    commands:
      # Installs Git
      - apt-get install -y git
  pre_build:
    commands:
      - git --version
  build:
    commands:
      - cd /opt && git clone https://github.com/shylaharild/deloitte-test.git
      - cd /opt/deloitte-test
      - mkdir -p /opt/images
      - cp -r /opt/deloitte-test/random-number/* /opt/images/
      - cd /opt/images/ && zip -r /opt/random-number-v${tag_number}.zip ./*
  post_build:
    commands:
      - aws s3 cp /opt/random-number-v${tag_number}.zip s3://python-random-number/dev/
```
> The above given code is just an example. It will not work if used in the CodeBuild Build Project

## 3. Integration of multiple terraform modules, with abstraction, rather than a monolith

I was not able to use Terraform for this task. My knowledge of Terraform modules is very limited. I have a theoretical knowledge of how Terraform works and very limited practical knowledge with only examples on how to create EC2 instances and required components like VPCs, Subnets, Security Groups for the EC2 Instance. I would like to learn more about it with real-time applications because there is nothing like on-job training. All my CloudFormation experience is from on-job training.

However, I have created 2 separate CloudFormation templated for this task. One to create the S3 bucket for the application archives and another one to create the AWS Lambda functions, API Gateway and other resources. Each template does its own job  and can work individually. Also, the resource in one of the stack can be imported into the other one such that we don't need to explicitly mention the resource into the other stack.

## 4. Git history of the lifecycle of the development

The commit history can be found in this link https://github.com/shylaharild/deloitte-test/commits/master
