from fastapi import FastAPI, UploadFile, File
import shutil, os
from genai.report_agent import generate_report

app = FastAPI(title="Pothole GenAI Report API")

@app.post("/report")
async def report(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        result = generate_report(temp_path)
    finally:
        os.remove(temp_path)
    return {"report": result}
