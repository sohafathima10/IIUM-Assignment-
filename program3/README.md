# Face Detection App (Tkinter & OpenCV)

This Python GUI application detects facial features (eyes and nose tip) in images using OpenCV's Haar cascades. It allows you to browse through images, view detected features, and save the processed output.

## Features

- Loads images from a folder and displays them in a GUI
- Detects faces, eyes (blue circles), and nose tip (red circle)
- Browse images with Previous/Next buttons
- Save processed images with detected features
- User-friendly interface built with Tkinter

## Requirements

- Python 3.8+
- OpenCV (`cv2`)
- Pillow (`PIL`)
- Tkinter (included with Python)

Install dependencies:
```
pip install opencv-python pillow
```

## How to Use

1. **Prepare your images:**  
   Place your face images in the folder `program3/images` (or change the path in the script).

2. **Run the application:**
   ```
   python face_detection_app.py
   ```

3. **Browse and Save:**  
   - Use "⬅ Previous" and "Next ➡" to browse images.
   - Click "💾 Save Output" to save the processed image with detected features to the `output` folder.

## Output

- Eyes are marked with blue circles.
- Nose tip is marked with a red circle.
- Saved images are stored in the `output` folder next to the script.

## Files

- `face_detection_app.py` — Main application file

---

**Author:**  
IIUM Assignment  
September 2025