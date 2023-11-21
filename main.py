from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import boto3
from botocore.exceptions import NoCredentialsError
import shutil
import os

app = FastAPI()
s3_client = boto3.client('s3', region_name='ap-south-1')
bucket_name = 'YOUR_S3_BUCKET_NAME'

def delete_local_file(filename):
    try:
        os.remove(filename)
        print(f"The file {filename} has been deleted.")
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

async def upload_to_aws(file, bucket, s3_file):
    try:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        s3_client.upload_file(file.filename, bucket, s3_file)
        return True
    except FileNotFoundError:
        return False
    except NoCredentialsError:
        return False

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    upload_success = await upload_to_aws(file, bucket_name, file.filename)
    if upload_success:
        delete_local_file(file.filename)
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully"})
    else:
        return JSONResponse(status_code=500, content={"message": "Failed to upload file"})

@app.get("/image/{image_name}")
async def get_image(image_name: str):
    try:
        # Get the S3 object
        file = s3_client.get_object(Bucket=bucket_name, Key=image_name)
        
        # Stream the file directly from S3
        return StreamingResponse(file['Body'], media_type='image/jpeg')
    
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Image not found")
    except NoCredentialsError:
        raise HTTPException(status_code=401, detail="Credentials not available")
