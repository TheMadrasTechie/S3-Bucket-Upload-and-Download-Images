from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from S3_process import upload_file_to_s3, get_image_from_s3
from pdf_3_process import save_pdf_with_unique_name, retrieve_pdf_content
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from io import BytesIO
from pdf_3_process import save_pdf_with_unique_name, retrieve_pdf_content
app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read file contents
        file_bytes = await file.read()
        
        # Get file extension
        file_extension = file.filename.split(".")[-1]
        
        # Upload file to S3
        unique_image_name = upload_file_to_s3(file_bytes, file_extension)
        
        return {"message": "Image uploaded successfully", "image_id": unique_image_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@app.get("/image/{image_id}/")
async def get_image(image_id: str):
    try:
        # Retrieve image data from S3
        image_data = get_image_from_s3(image_id)
        
        # Create a response with image content
        response = Response(content=image_data, media_type="image/png")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve image: {str(e)}")


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Read the file content directly
        file_content = await file.read()

        # Save the PDF to S3 with a unique name
        unique_name = save_pdf_with_unique_name(file_content, file.filename)
        
        return {"status": "success", "unique_name": unique_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/retrieve_pdf/{pdf_name}")
async def get_pdf(pdf_name: str):
    try:
        pdf_content = retrieve_pdf_content(pdf_name)
        return Response(content=pdf_content, media_type="application/pdf")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))