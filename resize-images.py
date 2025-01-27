import cv2
import os
from PIL import Image
import numpy as np

def create_directories():
    """Create input and output directories if they don't exist."""
    os.makedirs("pics_in", exist_ok=True)
    os.makedirs("pics_out", exist_ok=True)

def detect_faces(image):
    """Detect faces in the image using OpenCV's face detection."""
    # Convert PIL Image to OpenCV format
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Load both face and upper body cascade classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY),
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    return faces

def get_head_boundaries(faces, image_width, image_height):
    """Get the boundaries that include the entire head for all detected faces."""
    if len(faces) == 0:
        return None
    
    # Get the boundaries of all faces
    x_min = min(face[0] for face in faces)
    y_min = min(face[1] for face in faces)
    x_max = max(face[0] + face[2] for face in faces)
    y_max = max(face[1] + face[3] for face in faces)
    
    # Calculate face height and add extra padding for the entire head
    face_height = y_max - y_min
    
    # Add padding:
    # - Top: 100% of face height for hair and head top
    # - Bottom: 20% of face height for chin
    # - Sides: 50% of face width for ears and hair
    padding_top = face_height
    padding_bottom = int(face_height * 0.2)
    padding_sides = int((x_max - x_min) * 0.5)
    
    x_min = max(0, x_min - padding_sides)
    y_min = max(0, y_min - padding_top)
    x_max = min(image_width, x_max + padding_sides)
    y_max = min(image_height, y_max + padding_bottom)
    
    return (x_min, y_min, x_max, y_max)

def resize_and_crop_image(image_path, target_width=1920, target_height=1080):
    """Resize and crop image to target dimensions while preserving entire heads."""
    # Open the image
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get original dimensions
        width, height = img.size
        
        # Detect faces
        faces = detect_faces(img)
        head_bounds = get_head_boundaries(faces, width, height)
        
        # Calculate target aspect ratio
        target_ratio = target_width / target_height
        current_ratio = width / height
        
        # Calculate new dimensions for cropping
        if current_ratio > target_ratio:
            # Image is wider than target ratio
            new_height = height
            new_width = int(height * target_ratio)
        else:
            # Image is taller than target ratio
            new_width = width
            new_height = int(width / target_ratio)
        
        # If faces were detected, ensure entire heads are included in the crop
        if head_bounds:
            x_min, y_min, x_max, y_max = head_bounds
            
            # Calculate center of heads
            head_center_x = (x_min + x_max) // 2
            head_center_y = (y_min + y_max) // 2
            
            # Calculate crop boundaries
            half_width = new_width // 2
            half_height = new_height // 2
            
            # Ensure heads are in the frame
            x1 = min(max(head_center_x - half_width, 0), width - new_width)
            y1 = min(max(head_center_y - half_height, 0), height - new_height)
        else:
            # No faces detected, center crop
            x1 = (width - new_width) // 2
            y1 = (height - new_height) // 2
        
        # Crop the image
        x2 = x1 + new_width
        y2 = y1 + new_height
        img_cropped = img.crop((x1, y1, x2, y2))
        
        # Resize to final dimensions
        img_resized = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        return img_resized

def process_images():
    """Process all images in the input directory."""
    # Ensure directories exist
    create_directories()
    
    # Get list of image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    input_files = [f for f in os.listdir('pics_in') 
                  if f.lower().endswith(image_extensions)]
    
    if not input_files:
        print("No image files found in 'pics_in' directory!")
        return
    
    # Process each image
    for filename in input_files:
        try:
            input_path = os.path.join('pics_in', filename)
            output_path = os.path.join('pics_out', f'resized_{filename}')
            
            print(f"Processing {filename}...")
            resized_img = resize_and_crop_image(input_path)
            resized_img.save(output_path, quality=95)
            print(f"Saved resized image to {output_path}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    process_images()
