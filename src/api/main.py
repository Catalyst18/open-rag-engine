from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from .models import FileInfo
from pydantic import ValidationError, BaseModel
from ingestion.pdf_processor import PdfProcessor 
from psql_db.connection import get_connection

app = FastAPI()

processing_status: dict[str, str] = {} #Todo: add backend to persist the status of the file processed

def run_pdf_background(filename: str):
    try:
        processor = PdfProcessor(filename)
        processor.run()
        processing_status[filename] = "done"
    except Exception as e:
        processing_status[filename] = "error"
        print(f"[PdfProcessor] ERROR for {filename}: {e}", flush=True)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile,background_tasks: BackgroundTasks) -> dict[str,str]|None:
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

@app.get("/files/{filename}/status")
def get_file_status(filename: str):
    status = processing_status.get(filename, "unknown")
    return {"file": filename, "status": status}


class User(BaseModel):
    name: str
    club: str

@app.post("/users")
def create_user(user: User):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name,club) VALUES(%s,%s) RETURNING id ;",
        (user.name,user.club)

    )
    user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return {
        "message": "User stored successfully",
        "user_id": user_id,
        "name": user.name,
        "club": user.club
    }    