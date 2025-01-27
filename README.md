# Image Resizer with Head Detection

This script resizes images to 1920x1080 pixels while ensuring that any detected heads are fully included in the final cropped image. It maintains the original orientation of images (portrait images remain in portrait mode).

## Requirements

- Python 3.6 or higher
- OpenCV
- Pillow
- NumPy

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Create a folder named `pics_in` (if it doesn't exist)
2. Place your input images in the `pics_in` folder
3. Run the script:
```bash
python resize-images.py
```
4. Resized images will be saved in the `pics_out` folder

## Features

- Automatically detects faces using OpenCV
- Ensures the entire head is included in the crop by adding smart padding:
  - 100% padding above face for hair and head top
  - 20% padding below face for chin
  - 50% padding on sides for ears and hair
- Maintains aspect ratio while resizing to 1920x1080
- Preserves original image orientation (portrait/landscape)
- Supports multiple image formats (jpg, jpeg, png, bmp, gif)
- Preserves image quality with high-quality resizing

## Notes

- If no faces are detected, the script will perform a center crop
- The script uses intelligent padding around detected faces to ensure the entire head is included
- Output images are saved with 95% JPEG quality to maintain image quality
- Portrait images are cropped but not rotated to maintain their original orientation
