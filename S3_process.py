import numpy as np
import boto3
from uuid import uuid4
from PIL import Image
import io
from fastapi import FastAPI, HTTPException, Response

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

def upload_file_to_s3(file_bytes, file_extension):
    try:
        unique_name = f"{uuid4()}.{file_extension}"
        
        # Upload the file to S3 bucket
        in_memory_file = io.BytesIO(file_bytes)
        s3_client.upload_fileobj(in_memory_file, BUCKET_NAME, unique_name)

        return unique_name.replace(f".{file_extension}", "")
    except Exception as e:
        raise Exception(f"Failed to save file to S3: {str(e)}")

# Example usage:
#Assuming `numpy_image` is a numpy array representing an image
#numpy_image = np.random.rand(100, 100, 3) * 255  # Example random image
#unique_image_name = upload_image_to_s3(numpy_image)
#print(f"Image saved with unique name: {unique_image_name}")


def get_image_from_s3(image_id: str):
    try:
        # Read the file from S3 bucket
        obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=f"{image_id}.png")
        image_data = obj['Body'].read()

        return image_data
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve image: {str(e)}")