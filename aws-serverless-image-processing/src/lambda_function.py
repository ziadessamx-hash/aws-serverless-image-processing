import json
import urllib.parse
import boto3
import os

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

DESTINATION_BUCKET = os.environ.get('DESTINATION_BUCKET', 'processed-images-destination-bucket')
METADATA_TABLE = os.environ.get('METADATA_TABLE', 'ImageMetadata')

def lambda_handler(event, context):
    for record in event['Records']:
        sqs_body = json.loads(record['body'])
        
        if 'Records' in sqs_body:
            for s3_record in sqs_body['Records']:
                source_bucket = s3_record['s3']['bucket']['name']
                object_key = urllib.parse.unquote_plus(s3_record['s3']['object']['key'], encoding='utf-8')
                file_size = s3_record['s3']['object']['size']
                
                print(f"Processing image {object_key} from bucket {source_bucket}")
                
                processed_key = f"processed-{object_key}"
                
                table = dynamodb.Table(METADATA_TABLE)
                table.put_item(
                    Item={
                        'ImageId': object_key,
                        'SourceBucket': source_bucket,
                        'DestinationBucket': DESTINATION_BUCKET,
                        'OriginalSize': file_size,
                        'Status': 'PROCESSED'
                    }
                )
                print(f"Successfully saved metadata for {object_key} to DynamoDB.")

    return {
        'statusCode': 200,
        'body': json.dumps('Image processing pipeline executed successfully!')
    }