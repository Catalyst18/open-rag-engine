from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from .models import FileInfo
from pydantic import ValidationError
from ingestion.pdf_processor import PdfProcessor
import os

app = FastAPI()

# added status tracking dictionaries seperately for pdf and video files
pdf_status: dict[str, str] = {}
video_status: dict[str, str] = {}

Upload_video_dir = "/app/src/uploaded_videos"
os.makedirs(Upload_video_dir, exist_ok=True)


# background task to process pdf files
def run_pdf_background(filename: str):
    try:
        processor = PdfProcessor(filename)
        processor.run()
        pdf_status[filename] = "done"
    except Exception as e:
        pdf_status[filename] = "error"
        print(f"[PdfProcessor] ERROR for {filename}: {e}", flush=True)

# background task to process video files
def run_video_background(filename: str):
    try:
        # need to find right processor for videofile
        # need to connect with ad, vd.py....
        video_status[filename] = "done"
    except Exception as e:
        video_status[filename] = "error"
        print(f"[VideoProcessor] ERROR for {filename}: {e}", flush=True)

# endpoint to upload pdf files
@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile,
    background_tasks: BackgroundTasks
) -> dict[str, str] | None:

    total = 0
    chunk = await file.read(1024 * 64)
    while chunk:
        total += len(chunk)
        chunk = await file.read(1024 * 64)
    await file.seek(0)
    if  file.filename:
        try:
            info = FileInfo(file=file.filename, size=total)
            info.save_file(file=file)
            background_tasks.add_task(run_pdf_background, file.filename)
        except ValidationError as exc:
            raise HTTPException(status_code=400, detail=str(exc.errors()))

        return  {"file": file.filename, "status": "processing"}

# endpoint to upload video files
@app.post("/upload/video")
async def upload_video_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks
):

    try:
        file_path = os.path.join(Upload_video_dir, file.filename)

        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)

        video_status[file.filename] = "processing"
        background_tasks.add_task(run_video_background, file.filename)

        return {"file": file.filename, "status": "processing"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# endpoint to get pdf processing status
@app.get("/pdf/{filename}/status")
def get_pdf_status(filename: str):
    return {
        "file": filename,
        "status": pdf_status.get(filename, "unknown")
    }

# endpoint to get video processing status
@app.get("/video/{filename}/status")
def get_video_status(filename: str):
    return {
        "file": filename,
        "status": video_status.get(filename, "unknown")
    }
