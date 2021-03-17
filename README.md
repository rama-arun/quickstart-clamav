# Project README
## Pre-requisites
1. Create a new image repository using AWS console or CLI with command
    `aws ecr create-repository --repository-name $IMAGE_REPO_NAME--image-tag-mutability IMMUTABLE--image-scanning-configuration scanOnPush=true`
2. Clone this repository
3. Update the image repository name in buildspec.yml at both line 21 and 22
4. Create your personal access token from [github](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) 
5. Store your token in AWS SecretsManager and save the secret name and key
6. Replace the secretname and key name at line 148 in template.yml
7. After the stack is deployed, add VPC, subnet and securitygroup for your codebuild project so build instance can reach internet to download packages

## Runtime Architecture Flow
1. New objects are placed in S3 bucket in designated folder
2. S3 triggers the lambda function 
3. Lambda function pulls the latest docker image from ECR registry
4. Lambda function scans the new object for viruses using ClamAV open source

## Development Architecture Flow
- **A.** Developer checks in the code into GitHub repository
- **B.** GitHub WebHook triggers the CodeBuild build project
- **C.** CodeBuild build project packages the application into updated container image and uploads to ECR
- **D.** CodeBuild build project updates the lambda function to use latest image
- **E.** Timer Event runs every 24 hours and triggers the build. Build process will update the container image with latest virus definitions, publishes to ECR and updates the lambda function

## TODO:
1. Make this solution work with one or more existing bucket(s)
2. Input VPC to allow codebuild to reach internet and avoid manual modification of codebuild project
3. Add support for S3 object versions
4. Trim down the IAM permissions across the solution