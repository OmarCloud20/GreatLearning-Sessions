#******************************************************************************************
# Author - Omar A Omar
# The lambda is to extract texts from uploaded PDFs to source S3 bucket and upload results
# to targte destination bucket.
# The lambda is using AWS Textract boto3 library.
#
# Steps:
# 1. Add the target bucket to lambda environment variable: Name: [TARGET_BUCKET] Value: [target_bucket_name]
# 2. Add AmazonTextractFullAccess policy to the lambda role
# 3. Add "s3:GetObject" and "s3:PutObject" actions to the lambda role
#******************************************************************************************

import boto3
import os
import json

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
    # upload the extracted text to a new S3 bucket
    text = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text.append(item['Text'])

    s3client.put_object(Bucket=targetBucket, Key=key+".txt", Body='\n'.join(text))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Text extraction is completed successfully')
    }
