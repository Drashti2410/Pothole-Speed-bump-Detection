# Pothole & Speed Bump Detection

## Overview

This repository contains code, model weights, and dataset for detecting potholes and speed bumps in road images and video using a YOLO-style object detection model. It supports quick inference with the provided `best.pt` weights, a FastAPI detection service, and a GenAI layer (RAG + LangChain agent + MCP server) that turns detections into maintenance reports grounded in policy and incident history documents.

## Features

- Detects: `pothole` and `speed bump` classes
- Ready-to-run weights included (`best.pt`)
- Example notebook for dataset inspection and inference
- Training logs and experiment artifacts included
- FastAPI `/detect` endpoint for image-based inference, containerized with Docker
- GenAI reporting layer: RAG over road maintenance policy/incident docs, a LangChain agent that combines detection with policy lookup, a `/report` endpoint, and an MCP server exposing the same tools
- CI pipeline (GitHub Actions) running tests and a Docker build on every push

## Quick Start

1. Install dependencies (uses `uv`, with `pyproject.toml`/`uv.lock`):

```bash
uv sync
```

2. Run inference (example):

```bash
# Replace source with an image, folder or video
uv run detect.py --weights "Pothole-Speed bump Detection Code/best.pt" --source path/to/images_or_video --conf 0.25 --save-txt
```

3. Open the interactive demo and examples in the notebook:

- `pothole_detection.ipynb`

## Detection API

A FastAPI service wraps the YOLO model for image-based inference.

```bash
cd "Pothole-Speed bump Detection Code"
uv run uvicorn api.main:app --reload
```

- `GET /health` — service health check
- `POST /detect` — upload an image file (`file`) with optional `conf` query param (default `0.25`); returns detections, count, and latency

Run with Docker instead (build from the repo root, since the image installs deps via `uv` from the root `pyproject.toml`/`uv.lock`):

```bash
docker build -t pothole-api -f "Pothole-Speed bump Detection Code/Dockerfile" .
docker run -p 8000:8000 pothole-api
```

## GenAI Reporting Layer

Located in `Pothole-Speed bump Detection Code/genai/`, this layer generates maintenance reports by combining detection results with retrieval-augmented lookups over the docs in `docs/` (`road_maintenance_policy.txt`, `past_incident_log.txt`).

- `rag_chain.py` — builds a RetrievalQA chain (Chroma + OpenAI embeddings) over the policy/incident docs
- `report_agent.py` — a LangChain agent (`ZERO_SHOT_REACT_DESCRIPTION`) with `DetectPotholes` and `PolicyLookup` tools; `generate_report(image_path)` produces a 3-sentence maintenance report with a priority recommendation
- `main.py` — FastAPI `POST /report` endpoint that accepts an image upload and returns the generated report
- `mcp_server.py` — exposes `detect_potholes`, `check_maintenance_policy`, and `generate_maintenance_report` as MCP tools via `FastMCP`

Requires an `OPENAI_API_KEY` (loaded via `.env`). Run the report API with:

```bash
cd "Pothole-Speed bump Detection Code"
uv run uvicorn genai.main:app --reload
```

Run the MCP server standalone with:

```bash
uv run python -m genai.mcp_server
```

## Testing

```bash
cd "Pothole-Speed bump Detection Code"
uv run pytest tests/
```

- `tests/test_api.py` — detection endpoint tests
- `tests/test_genai.py` — RAG retrieval grounding tests (verifies answers are relevant and cite source documents)

## Files & Artifacts

- Model weights: `Pothole-Speed bump Detection Code/best.pt`
- Notebook demo: `Pothole-Speed bump Detection Code/pothole_detection.ipynb`
- Detection API: `Pothole-Speed bump Detection Code/api/`
- GenAI reporting layer: `Pothole-Speed bump Detection Code/genai/`
- Policy & incident source docs: `Pothole-Speed bump Detection Code/docs/`
- Training experiments and logs: `Pothole-Speed bump Detection Code/content/YOLOv11-Training/`
- Dataset splits and labels: `Pothole-Speed bump Detection Code/dataset/`

## Training (high-level)

1. Prepare dataset in YOLO format (images + labels).
2. Update `data.yaml` with class names and train/val paths.
3. Train using the training script or framework used for this project (check `content/YOLOv11-Training` for example args and config).

## Dataset Format

Dataset follows YOLO-style text label files: each label file contains lines with `class x_center y_center width height` normalized to image size. See the `dataset/` folder for train/val/test splits.

## Results & Logs

Training results and TensorBoard event files are located in `content/YOLOv11-Training/pothole-speedbump-detect`.
