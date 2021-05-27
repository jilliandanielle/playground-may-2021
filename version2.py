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

        print('Bucket: ', bucket, '\nKey:',key)

        csv_file = s3.get_object(Bucket = bucket, Key = key)
        record_list = csv_file['Body'].read().decode('utf-8').split('\n')
        csv_reader = csv.reader(record_list, delimiter = ',', quotechar = '"')

        for row in csv_reader:
            movie_id = row[0]
            movie    = row[1]
            title    = row[2]
            year     = row[3]

            print('\nMovie_ID: ', movie_id, '\nMovie: ', movie, '\nTitle: ', title, '\nYear: ', year)

    except Exception as e:
        print(str(e))

        return {
            'statusCode' : 500,
            'body'       : json.dumps('Something went wrong!')
        }
    else:
        return {
            'statusCode' : 200,
            'body'       : json.dumps('CSV to DynamoDB Success!')
        }