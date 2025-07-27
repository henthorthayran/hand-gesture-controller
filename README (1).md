
# 🖐️ Face + Hand Gesture Controlled Device

## 📘 Project Report

**Main Project**: Object Detection and Classification  
**Subproject**: Hand Gesture Controller

---

## 🧩 Problem Statement

Traditional input devices like mouse and keyboard are not always practical or accessible. There's a growing demand for **touchless interaction**, especially:

- In post-COVID environments for hygiene
- For people with physical disabilities
- During teaching or presentations
- On systems without a touchpad (e.g., Raspberry Pi)

---

## 🎓 What We Learned

- **Linear Regression** with Gradient Descent
- **Regularization** to prevent overfitting
- **Neural Networks**: ANN & CNN
- **Backpropagation**, Activation Functions: ReLU, Sigmoid
- **PyTorch** framework
- **Data Augmentation** for improving datasets
- **YOLO** training for real-time object detection
- Working with **Roboflow** & custom datasets
- Using **OpenCV** for webcam integration
- Working with **LLMs** and **Agentic AI**

---

## 🛠️ Tools & Technologies Used

| Tool / Library        | Purpose                                |
|-----------------------|-----------------------------------------|
| Python                | Programming Language                    |
| FaceNet               | Face Recognition (InceptionResnetV1)    |
| OpenCV                | Video capture & processing              |
| MediaPipe             | Hand & Face landmark detection          |
| PyAutoGUI             | Mouse, Keyboard, Scroll, Volume Control |
| NumPy                 | Distance, Interpolation                 |
| Webcam                | Real-time input                         |

---

## 🧠 Project Architecture

```text
[ Webcam Frame (cv2) ]
         │
         ▼
[ Face Detection (MediaPipe) ]
         │
         ├─► Crop Face
         │     ▼
         │ [ InceptionResnetV1 (FaceNet) → 512D Embedding ]
         │     ▼
         │ [ Compare with Saved Embeddings → Identity ]
         └────► If identity == "punit" → Allow gesture control

         ▼
[ Hand Detection (MediaPipe Hands) ]
         ▼
[ Landmark Extraction & Gesture Analysis (Custom logic) ]
         ▼
[ Action Execution (pyautogui) ]
      - Mouse control
      - Zoom
      - Volume
      - Scroll
      - Double Click
```

---

## 🌍 Real-World Applications

- 🏠 **Smart Home**: Gesture control for lights, fans, media  
- 🧑‍💻 **Touchless Computers**: For accessibility or hygiene  
- 🚗 **Vehicles**: Adjust volume/calls with gestures  
- 🏫 **Classrooms**: Gesture-based slide/presentation control  
- 🏥 **Hospitals**: Surgeons interact without touching surfaces  
- 🔐 **Secure Kiosks**: Face unlock + gesture navigation  
- 🕶️ **AR/VR Interfaces**: Natural control in immersive apps  
- 📹 **Surveillance**: Allow only known users to control panels  
- 🏭 **Industrial Monitoring**: Gesture dashboard navigation  
- 📱 **Mobile Apps**: Gesture-based controls using webcam

---

## ⚠️ Challenges Faced

| # | Issue                         | Cause                                                   | Fix                                                                 |
|---|-------------------------------|----------------------------------------------------------|----------------------------------------------------------------------|
| 1 | 🕒 Slow Response Time         | Model inference, frame lag                              | Reduce resolution, optimize cooldown, consider threading            |
| 2 | 🖱 Double Click Unreliable     | Gesture held too short/long                             | Use stable gestures (e.g. two-tap), improve timing logic            |
| 3 | 🔁 Too Many Actions Triggering| Multiple gesture matches                                | Use gesture priority or modes                                       |
| 4 | 📜 Scroll Didn’t Work Properly| Finger Y-position inconsistent                          | Widen Y-thresholds or use gesture speed                             |
| 5 | 🔍 Zoom In/Out Glitches       | Unstable distance thresholds                            | Smooth distance with averaging, adjust thresholds                   |
| 6 | ⚡ Fast Start, Then Delay     | Cooldown blocks rapid repeated gestures                 | Refine cooldown logic, detect gesture *change*, not just time-based |

---

## 🔮 Future Work

- 📺 Integration with **Smart Home Devices**
- 🍓 Deployment on **Raspberry Pi**
- ✌️ **Multi-hand & Multi-user Support**
- 🗣️ **Voice + Gesture Hybrid Control**
- 🧠 **Gesture Customization**
- 🌐 Expand to **Mobile, Smart TVs, AR/VR, IoT**

---

## 📦 requirements.txt

```txt
opencv-python
mediapipe
pyautogui
numpy
torch
facenet-pytorch
```

---

## ✅ How to Use

1. Clone this repository  
2. Run `pip install -r requirements.txt`  
3. Place your face embedding files (`*.pt`) in the same folder  
4. Run the main Python script  
5. Use gestures after face recognition (Punit is authenticated)

---

