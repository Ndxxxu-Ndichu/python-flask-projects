import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAYGIXF7RW7ASRCYK3'
SECRET_KEY = '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'

def upload_file (file_name, bucket):
    object_name = file_name
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response