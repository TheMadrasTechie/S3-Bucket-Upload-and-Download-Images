from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse, Response
import boto3
from botocore.exceptions import NoCredentialsError
import shutil
import os
import json

app = FastAPI()
s3_client = boto3.client('s3', region_name='ap-south-1')
bucket_name = 'YOUR_S3_BUCKET'

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

@app.post("/upload-json/")
async def upload_json(request: Request):
    json_data = await request.json()
    json_filename = f"{json_data['name']}.json"  # You can use a unique identifier

    try:
        s3_client.put_object(Bucket=bucket_name, Key=json_filename, Body=json.dumps(json_data))
        return JSONResponse(status_code=200, content={"message": "JSON uploaded successfully"})
    except NoCredentialsError:
        return JSONResponse(status_code=500, content={"message": "Failed to upload JSON"})

@app.post("/upload-json-file/")
async def upload_json_file(file: UploadFile = File(...)):
    if file.content_type != 'application/json':
        return JSONResponse(status_code=400, content={"message": "Invalid file type"})

    json_content = await file.read()
    json_filename = file.filename

    try:
        s3_client.put_object(Bucket=bucket_name, Key=json_filename, Body=json_content)
        return JSONResponse(status_code=200, content={"message": "JSON file uploaded successfully"})
    except NoCredentialsError:
        return JSONResponse(status_code=500, content={"message": "Failed to upload JSON file"})

@app.get("/json/{json_name}")
async def get_json(json_name: str):
    try:
        file = s3_client.get_object(Bucket=bucket_name, Key=f"{json_name}.json")
        json_data = file['Body'].read().decode('utf-8')
        return Response(content=json_data, media_type="application/json")
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="JSON not found")
    except NoCredentialsError:
        raise HTTPException(status_code=401, detail="Credentials not available")