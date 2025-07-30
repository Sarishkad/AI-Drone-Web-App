# YOLOv8 Environment Setup (env1)

## Project Setup

```bash
# Create a project directory
mkdir testYolo
cd testYolo

# Create a virtual environment
python -m venv env1

# Activate the virtual environment (for Windows)
env1\Scripts\activate.bat
```

## Package Installation

```bash
# Install setuptools
pip install setuptools

# Install PyTorch with CUDA support (use the command suitable for your GPU & CUDA version from the link below)
# https://pytorch.org/get-started/locally/

# Example for CUDA 11.8 (change if needed):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Or install CPU-only version:
# pip install torch torchvision torchaudio

# Install YOLOv8 from the official Ultralytics GitHub repository
pip install git+https://github.com/ultralytics/ultralytics.git@main
```

## Testing Installation

```bash
# Test if YOLOv8 is installed correctly
yolo help

# Run a sample prediction
yolo task=detect mode=predict model=yolov8n.pt source="https://ultralytics.com/images/bus.jpg"
```

## Environment Management

```bash
# To deactivate the environment
deactivate
```

## Notes

- Make sure to check the [PyTorch installation page](https://pytorch.org/get-started/locally/) for the correct CUDA version command
- The sample prediction will download the YOLOv8n model automatically on first run
- This setup creates an isolated environment to avoid package conflicts