FROM python:3.11-slim

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY api/ ./api
COPY "Pothole-Speed bump Detection Code/best.pt" "Pothole-Speed bump Detection Code/best.pt"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]