# Vehicle Attribute Analyzer

This Python project analyzes traffic images to detect vehicles, estimate their color, and determine lane position using YOLOv8 and OpenCV.

## Features

- Detects vehicles (car, motorcycle, bus, truck) in images
- Estimates dominant color of each vehicle
- Determines lane position (Left/Right)
- Annotates images with bounding boxes and labels
- Saves results as JSON files

## Requirements

- Python 3.8+
- [ultralytics](https://docs.ultralytics.com/) (`YOLO`)
- OpenCV (`cv2`)
- NumPy

Install dependencies:
```
pip install ultralytics opencv-python numpy
```

## Usage

1. **Prepare your images:**  
   Place your traffic images in a folder (e.g., `traffic_images`).

2. **Edit the script:**  
   In `vehicle_attribute.py`, set the folder path:
   ```python
   folder = "traffic_images"  # <--- CHANGE this to your images folder path
   ```

3. **Run the script:**
   ```
   python vehicle_attribute.py
   ```

4. **Results:**  
   - Annotated images will be saved in `annotated_images/`
   - JSON results will be saved in `results/`

## Output Example

Each detected vehicle includes:
- Type (car, motorcycle, bus, truck)
- Bounding box coordinates
- Estimated color
- Lane position (Left/Right)

Example JSON:
```json
{
    "incoming_traffic": true,
    "outgoing_traffic": true,
    "vehicle_count": 2,
    "vehicles": [
        {
            "type": "car",
            "bbox": [100, 50, 200, 150],
            "color": "white",
            "lane": "Left",
            "make": null,
            "logo_bbox": null,
            "license_plate_present": false,
            "license_plate_bbox": null,
            "license_plate_color": null
        }
    ]
}
```

## Troubleshooting

- If you get errors about missing models, ensure you have internet access for YOLO to auto-download weights.
- If images are not processed, check your folder path and image formats.

---

**Author:**  
IIUM Assignment  
September 2025