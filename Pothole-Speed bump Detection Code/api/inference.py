from ultralytics import YOLO
from PIL import Image
import io

MODEL_PATH = "Pothole-Speed bump Detection Code/best.pt"
model = YOLO(MODEL_PATH)

def run_inference(image_bytes: bytes, conf: float = 0.25):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = model.predict(image, conf=conf, verbose=False)
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": model.names[int(box.cls)],
                "confidence": float(box.conf),
                "bbox": [float(x) for x in box.xyxy[0].tolist()]
            })
    return detections