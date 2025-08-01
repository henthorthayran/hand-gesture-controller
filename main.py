import cv2
import time
import pyautogui
import mediapipe as mp
import numpy as np
from facenet_pytorch import InceptionResnetV1
import torch

# Screen size
screen_w, screen_h = pyautogui.size()

# Load FaceNet model
# This model is pre-trained on the VGGFace2 dataset.
try:
    model = InceptionResnetV1(pretrained='vggface2').eval()
except Exception as e:
    print(f"Error loading FaceNet model: {e}")
    exit()

# Load known face embeddings
try:
    known_faces = {
        "punit": torch.load("punit_face.pt"),
        "chinmay": torch.load("chinmay_face.pt"),
        "shachin": torch.load("shachin_face.pt"),
        "pushkar": torch.load("pushkar_face.pt"),
    }
except FileNotFoundError as e:
    print(f"Error loading face embedding file: {e}")
    exit()

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.6)

#--- STATE & CONSTANTS ---  

# States and cooldowns
face_detected = False
last_zoom_time = 0
last_volume_time = 0
last_scroll_time = 0
last_mouse_move = 0

# Double click tracking

double_click_start = None
pyautogui.FAILSAFE = False
last_index_pos = None
mouse_mode_active = False

# Cooldown periods (in seconds)
ZOOM_COOLDOWN = 0.5
VOLUME_COOLDOWN = 0.4
SCROLL_COOLDOWN = 0.1
MOUSE_COOLDOWN = 0.01

# Double click duration
DOUBLE_CLICK_DURATION = 0.6
# Mouse sensitivity
MOUSE_SENSITIVITY = 3

# Function to get face embedding
def get_face_embedding(face_img):
    # Preprocess the face image for the model
    face_img = cv2.resize(face_img, (160, 160))
    face_img = np.transpose(face_img, (2, 0, 1)) / 255.0
    face_tensor = torch.tensor(face_img, dtype=torch.float32).unsqueeze(0)
    return model(face_tensor).detach()

# Gesture utils
def fingers_up(lmList):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = [lmList[tip_ids[0]][0] > lmList[tip_ids[0] - 1][0]]
    fingers += [lmList[tip_ids[i]][1] < lmList[tip_ids[i] - 2][1] for i in range(1, 5)]
    return fingers

# Function to calculate distance and center between two points
def get_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))
# Function to get the center point between two points
def get_center(p1, p2):
    return tuple(np.mean([p1, p2], axis=0).astype(int))

# Camera capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    current_time = time.time()

    # Face detection only once
    if not face_detected:
        result_face = face_detection.process(rgb)
        if result_face.detections:
            for detection in result_face.detections:
                bboxC = detection.location_data.relative_bounding_box
                x1 = max(0, int(bboxC.xmin * w))
                y1 = max(0, int(bboxC.ymin * h))
                x2 = min(w, int(x1 + bboxC.width * w))
                y2 = min(h, int(y1 + bboxC.height * h))
                face_img = frame[y1:y2, x1:x2]

                if face_img.size == 0:
                    continue

                # Get face embedding
                embedding = get_face_embedding(face_img)
                min_dist = float('inf')
                identity = "Unknown"

                # Compare with known faces
                for name, known_embedding in known_faces.items():
                    dist = torch.dist(embedding, known_embedding).item()
                    # If distance is below a threshold (0.8), we have a potential match
                    if dist < min_dist and dist < 0.8:
                        min_dist = dist
                        identity = name

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.putText(frame, identity, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                if identity == "punit":
                    face_detected = True
                    print("✅ Punit recognized — gesture control enabled")

    if face_detected:
        result_hands = hands.process(rgb)
        if result_hands.multi_hand_landmarks:
            for handLms in result_hands.multi_hand_landmarks:
                lmList = [(int(lm.x * w), int(lm.y * h)) for lm in handLms.landmark]
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                if lmList:
                    fingers = fingers_up(lmList)

                    # Mouse pad mode
                    if fingers == [True, True, True, True, True]:
                        index_tip = lmList[5]
                        if not mouse_mode_active:
                            last_index_pos = index_tip
                            mouse_mode_active = True
                        else:
                            if last_index_pos and current_time - last_mouse_move > MOUSE_COOLDOWN:
                                dx = (index_tip[0] - last_index_pos[0]) * MOUSE_SENSITIVITY
                                dy = (index_tip[1] - last_index_pos[1]) * MOUSE_SENSITIVITY
                                pyautogui.moveRel(-dx, dy)
                                last_mouse_move = current_time
                            last_index_pos = index_tip
                    else:
                        mouse_mode_active = False

                    # Zoom
                    if fingers[1] and fingers[4] and not fingers[2] and not fingers[3]:
                        dist = get_distance(lmList[4], lmList[8])
                        if current_time - last_zoom_time > ZOOM_COOLDOWN:
                            if dist < 50:
                                print("Zoom Out")
                                pyautogui.hotkey('ctrl', '-')
                            elif dist > 90:
                                print("Zoom In")
                                pyautogui.hotkey('ctrl', '=')
                            last_zoom_time = current_time

                    # Volume control
                    if fingers == [True, True, False, False, False]:
                        if current_time - last_volume_time > VOLUME_COOLDOWN:
                            if lmList[4][1] < lmList[2][1]:
                                print("Volume Up")
                                pyautogui.press("volumeup")
                            else:
                                print("Volume Down")
                                pyautogui.press("volumedown")
                            last_volume_time = current_time

                    # Scroll control
                    if fingers == [False, True, True, False, False]:
                        index_tip_y = lmList[8][1]
                        if current_time - last_scroll_time > SCROLL_COOLDOWN:
                            if index_tip_y <= 80:
                                print("Scroll Up")
                                pyautogui.scroll(50)
                            elif index_tip_y >= 280:
                                print("Scroll Down")
                                pyautogui.scroll(-50)
                            last_scroll_time = current_time

                    # Double click
                    if fingers == [False, True, True, True, False]:
                        if double_click_start is None:
                            double_click_start = current_time
                        elif current_time - double_click_start >= DOUBLE_CLICK_DURATION:
                            print("Double Click")
                            pyautogui.doubleClick()
                            double_click_start = None
                    else:
                        double_click_start = None
        else:
            double_click_start = None

    cv2.imshow("Face + Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
