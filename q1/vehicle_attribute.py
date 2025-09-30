import cv2
import numpy as np
import os
from ultralytics import YOLO
import json

# ========== Utility Functions ==========

def get_dominant_color(roi):
    roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    data = roi_rgb.reshape((-1, 3)).astype(np.float32)

    _, labels, centers = cv2.kmeans(data, 1, None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
        10, cv2.KMEANS_RANDOM_CENTERS)

    return tuple(map(int, centers[0]))

def rgb_to_name(rgb):
    r, g, b = rgb
    if r > 200 and g > 200 and b > 200:
        return "white"
    elif r > 150 and g < 100 and b < 100:
        return "red"
    elif b > 150 and r < 100 and g < 100:
        return "blue"
    elif g > 150 and r < 100 and b < 100:
        return "green"
    else:
        return f"rgb{rgb}"

def get_lane(x_center, img_width):
    return "Left" if x_center < img_width / 2 else "Right"

def bbox_center(bbox):
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def annotate_image(img, vehicles):
    for v in vehicles:
        x1, y1, x2, y2 = v['bbox']
        label = f"{v['type']} ({v['color']}, {v['lane']})"

        # Draw bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw label background
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)

        # Put text label
        cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # Draw logo box
        if v['logo_bbox'] and v['make']:
            lx1, ly1, lx2, ly2 = v['logo_bbox']
            cv2.rectangle(img, (lx1, ly1), (lx2, ly2), (255, 0, 0), 2)
            cv2.putText(img, v['make'], (lx1, ly1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        # Draw license plate box
        if v['license_plate_present'] and v['license_plate_bbox']:
            px1, py1, px2, py2 = v['license_plate_bbox']
            cv2.rectangle(img, (px1, py1), (px2, py2), (0, 0, 255), 2)
            cv2.putText(img, f"Plate: {v['license_plate_color']}", (px1, py1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    return img

# ========== Main Class ==========

class VehicleSceneAnalyzer:
    def __init__(self):
        self.vehicle_model = YOLO('yolov8n.pt')  # Vehicle detection model
        self.logo_model = YOLO('yolo11n.pt')     # Logo detection model
        self.plate_model = YOLO("best.pt")  # License plate detection model
        self.vehicle_classes = ['car', 'motorcycle', 'bus', 'truck']
        self.logo_classes = self.logo_model.names

    def analyze(self, img):
        h, w = img.shape[:2]

        # Vehicle detection
        results = self.vehicle_model(img)[0]
        vehicles = []

        for box in results.boxes:
            cls_id = int(box.cls.item())
            cls_name = self.vehicle_model.names[cls_id]
            if cls_name not in self.vehicle_classes:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            roi = img[y1:y2, x1:x2]

            dom_rgb = get_dominant_color(roi)
            color_name = rgb_to_name(dom_rgb)
            cx, cy = bbox_center((x1, y1, x2, y2))
            lane = get_lane(cx, w)

            # Logo detection
            logo_result = self.logo_model(roi)[0]
            logo_bbox = None
            make = None
            if len(logo_result.boxes) > 0:
                best_logo = logo_result.boxes[0]
                lx1, ly1, lx2, ly2 = map(int, best_logo.xyxy[0].tolist())
                logo_cls = int(best_logo.cls.item())
                make = self.logo_classes[logo_cls]
                logo_bbox = [x1 + lx1, y1 + ly1, x1 + lx2, y1 + ly2]

            # License Plate detection
            plate_result = self.plate_model(roi)[0]
            license_plate_present = False
            license_plate_bbox = None
            license_plate_color = None
            if len(plate_result.boxes) > 0:
                best_plate = plate_result.boxes[0]
                px1, py1, px2, py2 = map(int, best_plate.xyxy[0].tolist())
                license_plate_present = True
                license_plate_bbox = [x1 + px1, y1 + py1, x1 + px2, y1 + py2]

                # Crop plate for color detection
                plate_roi = roi[py1:py2, px1:px2]
                if plate_roi.size > 0:
                    plate_rgb = get_dominant_color(plate_roi)
                    license_plate_color = rgb_to_name(plate_rgb)

            vehicles.append({
                "type": cls_name,
                "bbox": [x1, y1, x2, y2],
                "color": color_name,
                "lane": lane,
                "make": make,
                "logo_bbox": logo_bbox,
                "license_plate_present": license_plate_present,
                "license_plate_bbox": license_plate_bbox,
                "license_plate_color": license_plate_color
            })

        incoming = any(v['lane'] == 'Left' for v in vehicles)
        outgoing = any(v['lane'] == 'Right' for v in vehicles)

        summary = {
            "incoming_traffic": incoming,
            "outgoing_traffic": outgoing,
            "vehicle_count": len(vehicles),
            "vehicles": vehicles
        }

        return summary

# ========== Batch Processing Function ==========

def analyze_folder(folder_path, save_json=False, json_folder="results", save_annotated=True, annotated_folder="annotated_images"):
    analyzer = VehicleSceneAnalyzer()
    os.makedirs(json_folder, exist_ok=True)
    if save_annotated:
        os.makedirs(annotated_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Warning: Could not read {img_path}")
                continue

            result = analyzer.analyze(img)

            print(f"Results for {filename}:")
            print(json.dumps(result, indent=4))
            print("-" * 40)

            if save_json:
                json_path = os.path.join(json_folder, f"{os.path.splitext(filename)[0]}.json")
                with open(json_path, "w") as f:
                    json.dump(result, f, indent=4)

            if save_annotated:
                annotated_img = annotate_image(img.copy(), result['vehicles'])
                save_path = os.path.join(annotated_folder, filename)
                cv2.imwrite(save_path, annotated_img)

# ========== Run Batch Example ==========

if __name__ == "__main__":
    folder = "q1/traffic_images"  # Change to your folder path
    analyze_folder(folder, save_json=True, save_annotated=True)
