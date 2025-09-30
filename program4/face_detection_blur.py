import cv2
import datetime

# Load OpenCV's pre-trained face detector (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open video capture (0 = default webcam; replace with video source if needed)
cap = cv2.VideoCapture(0)

# Define video writer (set when saving is triggered)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None
saving = False

print("Press 's' to start/stop saving video.")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Blur each face
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
        frame[y:y+h, x:x+w] = blurred_face

    # Display the frame
    cv2.imshow('Face Blurring Feed', frame)

    # Save frame if saving is active
    if saving and out is not None:
        out.write(frame)

    # Handle keypresses
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        saving = not saving
        if saving:
            # Create new video file with timestamp
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            out = cv2.VideoWriter(f'output_{timestamp}.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
            print(f"[INFO] Saving started: output_{timestamp}.avi")
        else:
            out.release()
            out = None
            print("[INFO] Saving stopped.")

    elif key == ord('q'):
        break

# Cleanup
cap.release()
if out:
    out.release()
cv2.destroyAllWindows()
