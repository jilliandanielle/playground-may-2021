# DevOps Playground May 2021
In this session, you’ll learn how to write AWS Lambda functions in Python to interact with S3 and DynamoDB. We will be utilising the SDK for Python, known as Boto3. With Boto3, developers can create, configure, and manage AWS services through code. 

During this playground you will:
- Set up AWS Lambda to interact with other AWS services such as S3, DynamoDB, and CloudWatch
- Set up a trigger on S3 invoking the Lambda to take a CSV file and parse it to DynamoDB
- Configure permissions to allow the services to interact
- Utilise AWS CloudWatch
*************************
1. **_Give Permissions-Role
IAM roles needs lambda s3 permission and dynamnodb and cloudwatch logs_**
    - Navigate to IAM (Global region)
    - Click on **Roles** in left hand side
    - Click **Create Role**
    - Click **Lambda** Under _Use Cases_
    - In the search Bar type in _S3_
    - Select **Amazon S3 Full Access**
    - In the search bar type in _Dynamo_
    - Select **DynamoDBFullAccess**
    - In the search bar type in _CloudWatch_
    - Select **AWSOpsWorksCloudWatchLogs**
    - Next Tags. This is good practice! Add tags
        - Name: < your name >
    - Name Role - "playground-role-< yourname >"
    
    Check to make sure all 3 policies are there

2. **_Creating the S3 Bucket_** 

    S3 buckets are global and do not require a region. Each bucket name must be unique. 

    - Navigate to S3
    - Click **Create Bucket**
    - Name Bucket
        - S3 is global. They need to be unique
        - Naming convection: "playground-s3-< your name >"
    - Block all public access
    - Create Bucket
    
    As you can see, the bucket is empty
    
3. Create Lambda Function
    

    
    __**Testing**__



4. Code to connect the Lambda function to the S3 bucket
5. Create the DynamoDB Table
6. Code to connect the DynamoDB Table to the Lambda function