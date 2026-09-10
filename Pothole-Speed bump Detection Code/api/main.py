from fastapi import FastAPI, UploadFile, File, HTTPException, Query
import logging, time
from api.inference import run_inference

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Pothole & Speed Bump Detection API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/detect")
async def detect(file: UploadFile = File(...), conf: float = Query(default=0.25, ge=0.05, le=1.0)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    image_bytes = await file.read()
    start = time.time()
    try:
        detections = run_inference(image_bytes, conf)
    except Exception as e:
        logging.exception("Inference failed")
        raise HTTPException(status_code=500, detail=str(e))
    latency = time.time() - start
    logging.info(f"Detected {len(detections)} objects in {latency:.2f}s")
    return {"detections": detections, "count": len(detections), "latency_seconds": latency}