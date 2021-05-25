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

        print('\nBucket: ', bucket, '\nKey:',key)

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