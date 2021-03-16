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

TODO:
1. Make this solution work with one or more existing bucket(s)
2. Input VPC to allow codebuild to reach internet
3. Add support for S3 object versions
4. Trim down the IAM permissions across the solution

