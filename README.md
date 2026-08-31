# Pothole & Speed Bump Detection

## Overview

This repository contains code, model weights, and dataset for detecting potholes and speed bumps in road images and video using a YOLO-style object detection model. It supports quick inference with the provided `best.pt` weights and includes an example notebook for exploratory analysis and demo runs.

## Features

- Detects: `pothole` and `speed bump` classes
- Ready-to-run weights included (`best.pt`)
- Example notebook for dataset inspection and inference
- Training logs and experiment artifacts included

## Quick Start

1. Install dependencies (example):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # or install torch, torchvision, and yolov* deps
```

2. Run inference (example):

```bash
# Replace source with an image, folder or video
python detect.py --weights "Pothole-Speed bump Detection Code/best.pt" --source path/to/images_or_video --conf 0.25 --save-txt
```

3. Open the interactive demo and examples in the notebook:

- `pothole_detection.ipynb`

## Files & Artifacts

- Model weights: `Pothole-Speed bump Detection Code/best.pt`
- Notebook demo: `Pothole-Speed bump Detection Code/pothole_detection.ipynb`
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
