from fastapi.testclient import TestClient
from api.main import app
import io
from PIL import Image

client = TestClient(app)

def make_test_image():
    img = Image.new("RGB", (640, 480), color="gray")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

def test_health():
    assert client.get("/health").status_code == 200

def test_detect_valid_image():
    img = make_test_image()
    r = client.post("/detect", files={"file": ("test.jpg", img, "image/jpeg")})
    assert r.status_code == 200
    assert "detections" in r.json()

def test_detect_rejects_non_image():
    r = client.post("/detect", files={"file": ("test.txt", b"not an image", "text/plain")})
    assert r.status_code == 400

def test_detect_confidence_bounds():
    img = make_test_image()
    r = client.post("/detect?conf=2.0", files={"file": ("test.jpg", img, "image/jpeg")})
    assert r.status_code == 422  # out of range