# Face Detection & Blurring (Live Video)

This Python script uses OpenCV to detect faces in a live video feed (webcam) and blur them in real time. You can optionally save the processed video by pressing a key.

## Features

- Detects faces using Haar cascades
- Blurs each detected face in the video stream
- Displays the live feed with blurred faces
- Press `s` to start/stop saving the video to a file
- Press `q` to quit the application

## Requirements

- Python 3.8+
- OpenCV (`cv2`)

Install dependencies:
```
pip install opencv-python
```

## How to Use

1. Make sure your webcam is connected.
2. Run the script:
   ```
   python face_detection_blur.py
   ```
3. Controls:
   - Press **`s`** to start or stop saving the video. The output file will be named with a timestamp (e.g., `output_2025-09-29_14-30-00.avi`).
   - Press **`q`** to quit the application.

## Output

- The live video window will show faces blurred in real time.
- Saved videos will appear in the same folder as the script.

## Files

- `face_detection_blur.py` — Main script

---

**Author:**  
IIUM Assignment  
September 2025