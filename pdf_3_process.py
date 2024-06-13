import boto3
from uuid import uuid4
from botocore.exceptions import NoCredentialsError

# AWS credentials and bucket name
AWS_ACCESS_KEY = 'Your_key'
AWS_SECRET_KEY = 'Your_key'
BUCKET_NAME = 'bucket_name'
REGION = 'REGION'  # Mumbai region

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

def save_pdf_with_unique_name(file_content, file_name):
    try:
        unique_name = f"{uuid4()}.pdf"
        s3_client.put_object(Bucket=BUCKET_NAME, Key=unique_name, Body=file_content, ContentType='application/pdf')
        return unique_name
    except NoCredentialsError:
        raise Exception("Credentials not available for AWS S3.")

def retrieve_pdf_content(pdf_name):
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=pdf_name)
        return response['Body'].read()
    except s3_client.exceptions.ClientError:
        raise FileNotFoundError(f"No PDF found with the name: {pdf_name}")
