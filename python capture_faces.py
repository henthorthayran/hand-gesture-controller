import cv2
import mediapipe as mp
import numpy as np
from facenet_pytorch import InceptionResnetV1
import torch

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection

# Load pretrained FaceNet model
model = InceptionResnetV1(pretrained='vggface2').eval()

# Load and read image
img_path = "DATa.jpg"  # Change to your image path
image = cv2.imread(img_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect face using MediaPipe
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7) as face_detection:
    results = face_detection.process(image_rgb)
    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x1 = int(bboxC.xmin * iw)
            y1 = int(bboxC.ymin * ih)
            x2 = int(x1 + bboxC.width * iw)
            y2 = int(y1 + bboxC.height * ih)

            # Crop the face
            face_crop = image[y1:y2, x1:x2]
            if face_crop.size == 0:
                print("Face crop failed.")
                continue

            # Resize and preprocess
            face_crop = cv2.resize(face_crop, (160, 160))
            face_crop = np.transpose(face_crop, (2, 0, 1)) / 255.0
            face_tensor = torch.tensor(face_crop, dtype=torch.float32).unsqueeze(0)

            # Get embedding
            embedding = model(face_tensor).detach()
            print("Embedding shape:", embedding.shape)
            
            # Save embedding (optional)
            torch.save(embedding, "shachin_face.pt")
            print("Saved embedding to shachin_face.pt")

    else:
        print("No face detected.")
