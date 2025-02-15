import os
import boto3
import sys
from botocore.exceptions import NoCredentialsError

# AWS Credentials
S3_FOLDER = "spoof_images/"

# Local directory containing files
LOCAL_FOLDER = r"D:\\spoof images"

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_progress(chunk, file_size, uploaded):
    percentage = (uploaded / file_size) * 100
    sys.stdout.write(f"\rUploading... {percentage:.2f}% complete")
    sys.stdout.flush()

def upload_files_to_s3():
    if not os.path.exists(LOCAL_FOLDER):
        print(f"Folder {LOCAL_FOLDER} does not exist.")
        return
    
    files = [f for f in os.listdir(LOCAL_FOLDER) if os.path.isfile(os.path.join(LOCAL_FOLDER, f))]
    total_files = len(files)
    
    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(LOCAL_FOLDER, filename)
        s3_key = S3_FOLDER + filename  # S3 Key (path in bucket)
        try:
            file_size = os.path.getsize(file_path)
            print(f"Uploading {filename} ({index}/{total_files})")
            s3_client.upload_file(file_path, S3_BUCKET_NAME, s3_key, Callback=lambda bytes_transferred: upload_progress(bytes_transferred, file_size, bytes_transferred))
            print(f"\nCompleted uploading: {filename}")
        except NoCredentialsError:
            print("Credentials not available.")
        except Exception as e:
            print(f"Failed to upload {filename}: {e}")

if __name__ == "__main__":
    upload_files_to_s3()