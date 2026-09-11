FROM python:3.13-slim

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY ["Pothole-Speed bump Detection Code/api/", "./api/"]
COPY "Pothole-Speed bump Detection Code/best.pt" "Pothole-Speed bump Detection Code/best.pt"

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]