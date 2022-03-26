#******************************************************************************************
# Author - Nirmallya Mukherjee
# This lambda function will open an S3 trigger JSON, check the bucket and file details
# Use the S3 api to read the PDF file and use the tika library to extract the text content
# Log the text content and metadata in cloudwatch
#
# Imp - This function will need a timeout of 2mins (depending on the PDF size) and mem of 256MB
#       Create a custom role for lambda with the following specifications
#       "lambda-multirole" with "CloudWatchFullAccess" and "AmazonS3FullAccess" policies
#
#******************************************************************************************
import boto3
import json
import os
import logging
from pip._internal.utils.misc import get_installed_distributions

logger = logging.getLogger()
logger.setLevel(logging.INFO)

required_pkgs = ['tika']


def lambda_handler(event, context):
    logger.info('********************** Environment and Event variables are *********************')
    logger.info(os.environ)
    logger.info(event)

    installed_pkgs = [pkg.key for pkg in get_installed_distributions()]
    for package in required_pkgs:
        if package not in installed_pkgs:
            logger.error('Apache Tika dependency is not there. Exiting')
            return {
                'statusCode': 500,
                'body': json.dumps('Missing dependencies, aborting!')
            }

    logger.info('All dependencies found, environment is looking good. Proceeding ...')
    extract_content(event)

    return {
        'statusCode': 200,
        'body': json.dumps('Execution is now complete')
    }


def extract_content(event):
    import tika
    from tika import parser

    try:
        #Read the target bucket from the lambda environment variable
        targetBucket = os.environ['TARGET_BUCKET']
    except:
        targetBucket = "skl-dest"
    print('Target bucket is', targetBucket)

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print('The s3 bucket is', bucket, 'and the file name is', key)
    s3client = boto3.client('s3')
    response = s3client.get_object(Bucket=bucket, Key=key)
    pdffile = response["Body"]
    print('The binary pdf file type is', type(pdffile))

    rawcontent = parser.from_buffer(pdffile)
    print('The raw PDF content type is', type(rawcontent))
    meta = rawcontent["metadata"]
    print('Metadata is', meta)
    content = rawcontent['content']
    #After the content extraction there are too many \n at the top of the content; remove them all
    content = content.replace("\n\n", "")
    print('Content is', content)

    s3client.put_object(Bucket=targetBucket, Key=key+".txt", Body=content)

    print('All done, returning from extract content method')



