import cv2
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Define the GUI application class
class FaceDetectionApp:
    def __init__(self, root, input_dir="data/input/"):
        self.root = root
        self.root.title("Face Feature Points")

        self.input_dir = input_dir
        # Get list of image files in input directory
        self.image_files = [f for f in os.listdir(input_dir) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]
        self.current_index = 0

        # Show error and exit if no images found
        if not self.image_files:
            messagebox.showerror("Error", f"No images found in {input_dir}")
            root.destroy()
            return

        # UI Buttons: Previous, Next, Save Output
        self.prev_btn = tk.Button(root, text="⬅ Previous", command=self.show_previous)
        self.prev_btn.pack(side="left", padx=5)

        self.next_btn = tk.Button(root, text="Next ➡", command=self.show_next)
        self.next_btn.pack(side="right", padx=5)

        self.save_btn = tk.Button(root, text="💾 Save Output", command=self.save_output, state=tk.DISABLED)
        self.save_btn.pack(pady=5)

        # Labels for input and output images
        self.input_label = tk.Label(root, text="Input Image")
        self.input_label.pack()
        self.input_canvas = tk.Label(root)
        self.input_canvas.pack(side="left", padx=10)

        self.output_label = tk.Label(root, text="Output Image")
        self.output_label.pack()
        self.output_canvas = tk.Label(root)
        self.output_canvas.pack(side="right", padx=10)

        self.processed_image = None  # To hold the output image with annotations
        self.show_image()  # Load the first image

    # Load and display current image
    def show_image(self):
        img_path = os.path.join(self.input_dir, self.image_files[self.current_index])
        image = cv2.imread(img_path)

        # Show error if image can't be read
        if image is None:
            messagebox.showerror("Error", f"Could not open {img_path}")
            return

        # Display original image
        self.display_image(image, self.input_canvas, max_size=300)

        # Detect and annotate features (eyes and nose)
        processed = self.detect_features(image.copy())
        self.processed_image = processed

        # Display processed (output) image
        self.display_image(processed, self.output_canvas, max_size=300)

        # Enable save button
        self.save_btn.config(state=tk.NORMAL)
        self.root.title(f"Face Detection – {self.image_files[self.current_index]}")

    # Navigate to next image
    def show_next(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_image()

    # Navigate to previous image
    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    # Detect face, eyes, and nose tip in the image
    def detect_features(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]

            # Detect eyes only in the upper half of the face region
            upper_half = roi_gray[0:h//2, :]
            eyes = eye_cascade.detectMultiScale(upper_half)

            # Draw circles on first two detected eyes
            for (ex, ey, ew, eh) in eyes[:2]:
                eye_cx = x + ex + ew // 2
                eye_cy = y + ey + eh // 2
                cv2.circle(image, (eye_cx, eye_cy), 5, (255, 0, 0), -1)  # Blue circle

            # Approximate nose tip position
            nose_cx = x + w // 2
            nose_cy = y + int(h * 0.6)
            cv2.circle(image, (nose_cx, nose_cy), 5, (0, 0, 255), -1)  # Red circle

        return image

    # Display a given OpenCV image on a tkinter canvas
    def display_image(self, cv_img, canvas, max_size=300):
        img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        pil_img.thumbnail((max_size, max_size))  # Resize for display
        tk_img = ImageTk.PhotoImage(pil_img)
        canvas.config(image=tk_img)
        canvas.image = tk_img  # Keep reference to avoid garbage collection

    # Save the processed (output) image
    def save_output(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No output image to save!")
            return

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)

        # Generate output filename
        input_filename = self.image_files[self.current_index]
        name, ext = os.path.splitext(input_filename)
        output_filename = f"{name}_output{ext}"
        save_path = os.path.join(output_dir, output_filename)

        # Save the image
        cv2.imwrite(save_path, self.processed_image)
        messagebox.showinfo("Saved", f"✅ Output saved at:\n{save_path}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root, input_dir="program3/images")  # Change the path as needed
    root.mainloop()
