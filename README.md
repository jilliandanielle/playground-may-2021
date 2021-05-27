# DevOps Playground May 2021
In this session, you’ll learn how to write AWS Lambda functions in Python to interact with S3 and DynamoDB. We will be utilising the SDK for Python, known as Boto3. With Boto3, developers can create, configure, and manage AWS services through code. 

During this playground you will:
- Set up AWS Lambda to interact with other AWS services such as S3, DynamoDB, and CloudWatch
- Set up a trigger on S3 invoking the Lambda to take a CSV file and parse it to DynamoDB
- Configure permissions to allow the services to interact
- Utilise AWS CloudWatch
*************************
 1. **_Creating the S3 Bucket_** 

    S3 buckets are global and do not require a region. Each bucket name must be unique. 

    - Navigate to S3
    - Click **Create Bucket**
    - Name Bucket
        - S3 is global. They need to be unique
        - Naming convection: "playground-s3-*-panda"
        - Example: "playground-s3-silly-panda"
    - Block all public access
    - Create Bucket
    
    As you can see, the bucket is empty

2. **_Give Permissions-Role
IAM roles needs lambda s3 permission and dynamnodb and cloudwatch logs_**

    - Navigate to **IAM** (Global region)
    - Click on **Roles** in left hand side
    - Click **Create Role**
    - Click **Lambda** Under _Use Cases_
    - Next Permissions
    - In the search Bar type in _S3_
        - Select **Amazon S3 Full Access**
    - In the search bar type in _Dynamo_
        - Select **DynamoDBFullAccess**
    - In the search bar type in _CloudWatch_
        - Select **AWSOpsWorksCloudWatchLogs**
    - Next **Tags**. This is good practice! Add tags
        - Name: < your name >
    - Name Role - "playground-role-*-panda"
        - example "playground-role-silly-panda"
    
    Check to make sure all 3 policies are there
    
3. A **_Create Lambda Function_**
    - Navigate to Lambda
    - Make sure you are in the correct region < eu-west-2 >
    - Click **Create Function**
    - **Author From Scratch**
    - Function name- "playground-lambda-*-panda" (example "playground-lambda-silly-panda")
    - **Python 3.8**
    - Permissions
        - Use an existing role
        -  Find your role (playground-role-*-panda) 
    - **Create function**

    Check out that confirmation!

    
    _**3.B Adding a Trigger**_

    This step enables the Lambda function to be triggered by the event of uploading an item into our S3 bucket

    - Design- **Add Trigger**
    - Search- _S3_
    - Bucket- Search for the S3 bucket you created 
        - (playground-s3-*-panda)
    - Event Type- All 
    - Suffix- .csv
    - Prefix- (optional)
    - Click **Add**
    
Look for the confirmation. You can check the s3 details to make sure it is enabled.



4. _**Code to connect the Lambda function to the S3 bucket + Mocking an upload**_

- Copy the code below into **lambda_function.py**:

**Version 1**
```
import json
import csv
import boto3

def lambda_handler(event, context):
    region = 'eu-west-2'
    record_list = []

    try:
        s3 = boto3.client('s3')  
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print('\nBucket: ', bucket, '\nCSV File: ',key)

    except Exception as e:
        print(str(e))

    return {
        'statusCode':200,
        'body': json.dumps('CSV to DynamoDB Success!')
    }
```

Configure Test Event
- Event template
    - Search _S3_ 
    - Select _Amazon S3 Put_
- Event name
    - playgroundcsvtest
- Create
- Click **Test** 
- Check the *Execution Results* to see the results

Uploading a CSV file to S3 and checking CloudWatch
- Navigate back to S3 (open in new tab if not there already)
- Search for your bucket
- Upload the CSV file to your bucket
    - Check to make sure the upload is successful

- Navigate back to *Lambda*
- Click on the tab **Monitoring** 
- Scroll down to **CloudWatch Insights**
- Select the latest entry under **LogStream** (a new tab will open up)
- Check the logs for your **bucket name** and the **CSV file**

5. Reading the CSV file with Python using boto3.

**Version 2**
```
import json
import csv
import boto3

def lambda_handler(event, context):
    region = 'eu-west-2'
    record_list = []

    try:
        s3 = boto3.client('s3') 
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print('\nBucket: ', bucket, '\nCSV File: ',key)

        csv_file = s3.get_object(Bucket = bucket, Key= key)

        record_list = csv_file['Body'].read().decode('utf-8').split('\n')
        
        csv_reader = csv.reader(record_list, delimiter=',',quotechar='"')

        for row in csv_reader:
            movie_id = row[0]
            movie = row[1]
            title = row[2]
            year = row[3]

            print('\nMovie_ID: ', movie_id, '\nMovie: ', movie, '\nTitle: ', title, '\nYear: ', year)

    except Exception as e:
        print(str(e))

    return {
        'statusCode':200,
        'body': json.dumps('CSV to DynamoDB Success!')
    }
```

To mock test an upload 
- Navigate to Lambda
- Configure Test Events
- Under "S3" replace "example-bucket" with the name of your bucket
    - "playground-s3-silly-panda"
- Under "object" replace "test/key" with the name of the csv file 
    - playground-marvel.csv
- Save
- Click on test to simulate a CSV upload (trigger)
- Check the _Execution Results_
 

6. Create the DynamoDB Table
    - Navigate to DynamoDB in a new tab. Important! Make sure you are in the same region as your Lambda Function.
    - Click **Create table**.
    - Enter "playground-db-*-panda" for the **Table name**. (example: "playground-db-silly-panda")
    - Enter < actorid > for the **Partition key** and select < Number > for the key type. 
    - Add tags because it's good practice! name: jillian, purpose: playground
    - Leave the **Use default settings** box checked and choose **Create**.
    - Click on the tabs on top just to check there are no items. After we upload, the items will appear here

7. Add code to connect the DynamoDB to the Lambda Function

**Version 3**
```
import json
import csv
import boto3

def lambda_handler(event, context):
    region = 'eu-west-2'
    record_list = []

    try:
        s3 = boto3.client('s3') 

        dynamodb = boto3.client('dynamodb', region_name = region)

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print('\nBucket: ', bucket, '\nCSV File: ',key)

        csv_file = s3.get_object(Bucket = bucket, Key= key)

        record_list = csv_file['Body'].read().decode('utf-8').split('\n')

        
        csv_reader = csv.reader(record_list, delimiter=',',quotechar='"')

        for row in csv_reader:
            movie_id = row[0]
            movie = row[1]
            title = row[2]
            year = row[3]

            print('\nMovie_ID: ', movie_id, '\nMovie: ', movie, '\nTitle: ', title, '\nYear: ', year)

            add_to_db = dynamodb.put_item(
                TableName = 'playground-db-jillian',
                Item = {
                    'movie_id' : {'N':str(movie_id)},
                    'movie' : {'S':str(movie)},
                    'title' : {'S':str(title)},
                    'year' : {'N':str(year)},
                })
            print('\nSuccessfully added the records to the DynamoDB Table!\n')

    except Exception as e:
        print(str(e))

return {
    'statusCode':200,
    'body': json.dumps('CSV to DynamoDB Success!')
}
```


8. Check DynamoDB to make sure your items are there. You can also check out CLoudWatch and look through the logs. 



This concludes our lab today!