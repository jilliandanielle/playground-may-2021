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
        
        print('\nBucket: ', bucket, 'Key: ',key)

    except Exception as e:
        print(str(e))
        
        return {
            'statusCode': 500,
            'body': json.dumps('Eek, something went wrong!')
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Success!')
        }