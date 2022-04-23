#******************************************************************************************
# Author - Omar A Omar
# The lambda is to extract texts from uploaded files to source S3 bucket and upload results
# to the targte destination bucket. Also, it captures file name and extracted texts in DynamoDB
# The lambda is using AWS Textract boto3 library.
#
# Steps:
# 1. Add S3 target bucket to lambda environment variable: Name: [TARGET_BUCKET] Value: [target_bucket_name]
# 2. Add DynamoDB table to lambda environment variable: Name: [TABLE_NAME] Value: [dynamoDB_table_name]
# 3. Attach AmazonTextractFullAccess policy to the lambda role
# 4. Create inline DynamoDB policy to the lambda role. This allows the lambda to put and update items to DynamoDB table
# 5. Create inline S3 bucket policy to the lambda role. This allows the lambda to put and get objects from S3 bucket 
# Note: it's security best practice to grant least privilege 
#******************************************************************************************

import boto3
import os
import json
import datetime
import time


def lambda_handler(event, context):
    s3client = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print('The s3 bucket is', bucket, 'and the file name is', key)

    textract = boto3.client('textract')
    response = textract.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': bucket,
            'Name': key
        }
    })
    
    targetBucket = os.environ['TARGET_BUCKET']
    # upload the extracted text to target bucket S3 bucket
    text = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text.append(item['Text'])
            
    # join text instead of lines
    text ='\n'.join(text)

    s3client.put_object(Bucket=targetBucket, Key=key+".txt", Body='\n'.join(text))
    
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    # Put records to DynamoDB
    table_name = os.environ['TABLE_NAME']
    dynamo_client = boto3.client('dynamodb')
    table = boto3.resource('dynamodb').Table(table_name)
    item={'id':key, 'DateTime':timestamp, 'Text':text}
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Text extraction is completed successfully')
    }
