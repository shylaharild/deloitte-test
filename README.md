# Deloitte DevOps Recruitment Test

## Python generate ramdom number between 1 & 100

The programs generates random number between 1 and 100 when it is called using the HTTP GET endpoint. This program runs on AWS Lambda functions and uses the API Gateway to serve the HTTP endpoint.

Once you access the endpoint url, it will respond with the following.

```bash
{"message": "The number is 73"}
```

In the above example, the number "73" is generated by the python code in the lambda function invoked by the trigger when the user accessed the API Gateway endpoint

## Prerequisite and Assumptions

Assumptions that are made here are
* You have basic knowledge about the AWS, AWS CLI, Serverless model, CloudFormation, Lambda and API Gateway
* You understand the DevOps terminologies and have basic programming language understanding
* You have basic understanding of how to use Git and Github

The following are the prerequisites to carry on with this task
* Have an AWS Account and IAM User created with Programming & Console Access with required permissions
* Install & configure AWS CLI on the device that you're using to do this task
* Install git on the device that you're using to do this task

If you need to know more about creating an AWS Account and IAM User, follow the steps provided in the BONUS_POINTS.md file.

## CloudFormation templates

There are two CloudFormation templates involved in this task.

* deployment-resources.yaml
* random-number.yaml

Advantages of using CloudFormation, including but not limited to, are

1. Easy to use orchestration tool which creates all the required AWS resource within a click of the button
2. Enables us to maintain the record of the infrastructure created in the form of a file
3. Helps us to create versions of the infrastructure changes done
4. Converts the entire infrastructure into a code thus forming `Infrastructure as a Code`
5. In case of a disaster, this code helps us to spin up the same infrastructure within minutes
6. Helps us to have a backup copy of the infrastructure in a version controlled central repository

## deployment-resources.yaml
This CloudFormation template creates the S3 bucket for the application archives to be uploaded for the lambda function in the `random-number.yaml` template to access. This is made separate because the next template requires to archive to be available in the given location.

This stack can also be used to create the Continuous Integration and Continuous Deployment pipeline. Hence the name deployment-resources.

You can also skip this if you are planning to use the existing S3 bucket. Just make sure you upload the file into the S3 bucket with a definite Key so that the object is identified by the `random-number.yaml` stack.

eg: {existing-s3-bucket}/python-random-number/dev/random-number-v0.0.1.zip

Advantages of using S3 bucket for archives
1. Low cost object storage
2. Highly available, secure, reliable and easily accessible by the AWS resources
3. Can have multiple versions of the same file when Versioning is enabled
4. Can create different versions of the application as new files such that in case of issue we can roll back to earlier version
5. back up of the code & archive can be maintained at the SLA of 11 9's

## random-number.yaml
The CloudFormation template is the main template responsible to create Lambda function, API Gateway and other required resources for the application to run. This template has few parameters which is required for the resources mentioned in the Resource section to be created. This template also imports the output of the `deployment-resources.yaml` template so it is essential to have a successful creation of the `deployment-resources.yaml` stack before launching this template.

The parameters have default values in the template. You can edit it with the actual values and create stack using AWS Console access. However, it is advised to use the actual values in the command line so that you don have to change the file everytime you upload a new version of the application.

If you're using existing bucket, makes sure that the necessary parameter is mentioned when using the CLI.

Advantages of using AWS Lambda and API Gateway:
1. AWS Lambda reduces the infrastructure burden further by enabling the developers to concentrate only on code
2. Lambda takes care of provisioning the backend servers while the our responsibility is to provide the working code and required RAM and CPU resource as configuration
3. Eradicates the SSH access to the servers such that there is no more manual changes into servers directly done by the developers
4. Helps to maintain the stability of the code across the environments
5. Cost is greatly reduced as we pay only when the application is accessed, not for the idle hours
6. API Gateway helps to provide the easy access to the functions in the form of endpoint URLs
7. Enables region specific and edge location specific setup such that the application can be made available to the customers with lowest possible latency
8. Both Lambda and API Gateway can help the organisation to scale according to the traffic
9. Both can help in providing high availability, reliability and secure access of the application
10. They can also help to mitigate during DDoS or any other attack that would bring the service down when run using traditional infrastructure

The steps to use are provided below.

## How to deploy

The following are the AWS CLI commands you need to execute in the terminal. Clone the repository from the Github using the git command and navigate to the repository directory.

To create the `deployment-resources.yaml` stack, use the command
```bash
aws cloudformation create-stack --region us-east-1 --stack-name deployment-resources \
                  --template-body file://{path-to-directory}/deployment-resources.yaml \
                  --parameters ParameterKey=ApplicationName,ParameterValue=python-random-number \
                  --tags Key=Environment,Value=dev Key=Owner,Value=Sri
```
> You can replace Tag Values as per your desire. You have to be careful with the Parameter Values as it is used in the next stack's parameters as well.

The zip archive file for the application is available in the root folder of the repository. You can upload the archive file into the bucket using the command given below.

```bash
aws s3 cp {path-to-repository}/random-number-v0.0.1.zip s3://python-random-number/dev/ --region us-east-1
```

> Make sure that the archive is available in the S3 bucket before launching the random-number.yaml stack

To create the `random-number.yaml` stack, use the given command

```bash
aws cloudformation create-stack --region us-east-1 --stack-name python-random-number \
                  --template-body file://{path-to-directory}/random-number.yaml \
                  --parameters ParameterKey=ArchivePath,ParameterValue=dev ParameterKey=ArchiveFile,ParameterValue=random-number-v0.0.1.zip ParameterKey=ResourceStack,ParameterValue=deployment-resources \
                  --tags Key=Environment,Value=dev Key=Owner,Value=Sri
```

> ParameterValues are interdependent on both the stacks. Better not to change it.

If using existing S3 bucket

```bash
aws cloudformation create-stack --region us-east-1 --stack-name python-random-number \
                  --template-body file://{path-to-directory}/random-number.yaml \
                  --parameters ParameterKey=ArchivePath,ParameterValue=python-random-number/dev ParameterKey=ArchiveFile,ParameterValue=random-number-v0.0.1.zip ParameterKey=ExistingS3Bucket,ParameterValue={S3-Bucket-Name} \
                  --tags Key=Environment,Value=dev Key=Owner,Value=Sri
```

> Take caution while providing the parameter values.
> The Stack will rollback if the resource name doesn't matches with the one available in the AWS Account

Replace the operation name from `create-stack` to `update-stack`, if you want to update the stack with new version file.

```bash
aws cloudformation update-stack --region us-east-1 --stack-name python-random-number \
                  --template-body file://{path-to-directory}/random-number.yaml \
                  --parameters ParameterKey=ArchivePath,ParameterValue=dev ParameterKey=ArchiveFile,ParameterValue=random-number-v0.0.2.zip ParameterKey=ResourceStack,ParameterValue=deployment-resources \
                  --tags Key=Environment,Value=dev Key=Owner,Value=Sri
```

If you would like to verify the changes are going into stack, use `create-change-set` operation. You can see the list of changes in the AWS CloudFormation console.

```bash
aws cloudformation create-change-set --change-set-name {give-random-name-here} \
                  --region us-east-1 --stack-name python-random-number \
                  --template-body file://{path-to-directory}/random-number.yaml \
                  --parameters ParameterKey=ArchivePath,ParameterValue=dev ParameterKey=ArchiveFile,ParameterValue=random-number-v0.0.2.zip ParameterKey=ResourceStack,ParameterValue=deployment-resources \
                  --tags Key=Environment,Value=dev Key=Owner,Value=Sri
```

## Usage

To get the response, you need to access the API URL. If you have Created Custom DNS in the stack, you can use the domain name to access the endpoint.

If you navigate to the Outputs tab in the AWS CloudFormation Console, you can see the endpoint url listed in it. Copy it and paste it in the browser to get the response from the executed lambda function.

```bash
{"message": "The number is 73"}
```

When using curl command, you get the below response.

```bash
sri-mbp:deloitte-test sri$ curl https://r711hekib6.execute-api.us-east-1.amazonaws.com/dev/
{"message": "The number is 52"}
```

## Known Issues & Uncertainities
It is my responsibility as a DevOps professional to admit the issues and uncertainities in this code that I am aware of. I don't like to make a false pretence because I always believe in my favourite quote which is given below.

```
Loyalty is a two-way street. If I'm asking for it from you, then you're getting it from me.
```

The following are few that I am aware of.

* All my lambda experience comes from executing the tutorial examples and other AWS solutions given in their Answers webpage. I tried to implement this task with those knowledge and extra information from the AWS Documentation.
* The CloudFormation Stacks works fine with `CreateCustomDNS` set to false. Since I don't have a registered domain in my AWS Account, I couldn't test the code. However, I added it by reading the AWS docs and hoping that it will work.
* When I tried to add the domain record for the api endpoint manually and tried to access it through browser, I encountered SSL error. When I proceeded, the error I got was `{"message": "Forbidden"}`.
* I am not sure if the API endpoint is Region Specific. Though I have mentioned the `EndpointConfiguration` as `REGIONAL` for the ApiGateway, I feel there is more configuration to it to make it actual Region Specific.
* I feel that the CloudFormation templates might create a circulate dependency issue if we try to add the CI-CD pipeline. I may invest more time to design it properly.
* When I tried to check-in the code to my Github repository, I pushed all my changes directly to master. This is completely out of my usual process. I create branch to push the changes, do a PR review with another DevOps person and then merge it if there are no errors. Since I am the only person here I took the luxury of pushing all my changes to the master branch
* The goal was to provide a working solution at the end even though there are many dependencies that can be avoided.
