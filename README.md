# 🖐️ Face-Authenticated Gesture Control System  

A **real-time, touchless interaction system** that combines **face authentication** and **hand gesture recognition** to provide a secure and hygienic way to interact with your computer.  
Designed to minimize physical contact, improve accessibility, and enable futuristic human–computer interaction.  

---

## 📌 Problem Statement  

In public and shared environments (offices, classrooms, labs), constant contact with keyboards and mice can spread germs and create accessibility barriers for differently-abled individuals.  
This project aims to solve that problem by enabling **contactless, face-verified, gesture-based PC control** — ensuring both **security** and **hygiene**.  

---

## 🚀 Key Features  

✅ **Face Authentication:**  
- Uses **FaceNet (InceptionResnetV1)** pretrained on **VGGFace2** to verify user identity before enabling gestures.  
- Only authorized users can control the system, preventing unauthorized access.  

🖐️ **Gesture-Based Controls:**  
- **Virtual Mouse:** Move cursor with hand movement.  
- **Zoom In/Out:** Pinch gesture using thumb + index finger distance.  
- **Volume Control:** Thumb-up/down gestures for volume adjustment.  
- **Scroll & Double Click:** Two-finger scroll and three-finger double click.  
- **Custom Cooldowns:** Prevent accidental actions by adding configurable time gaps (e.g., 0.01s for mouse, 0.4s for volume).  

⚡ **Performance Optimized:**  
- Runs at **30+ FPS** on a standard webcam.  
- Maintains **< 50 ms latency** for smooth and responsive interaction.  

🛡 **Robustness:**  
- Handles missing face embeddings gracefully with proper error messages.  
- Works across multiple devices with minimal configuration.  
- Reduces false positives by **~70%** via tuned cooldowns and sensitivity.  

---

## 🔮 Future Work  

- **Voice Command Integration:** Combine gestures with speech for a fully hands-free system.  
- **AI-based Gesture Prediction:** Use ML models to make gesture recognition more adaptive and noise-tolerant.  
- **Mobile/IoT Integration:** Control smart devices and home automation systems.  
- **Customizable Gesture Mapping:** Allow users to map gestures to specific keyboard shortcuts or applications.  
- **Multi-User Support:** Recognize and switch profiles dynamically based on the authenticated user.  

---

## 🛠️ Tech Stack  

| Component           | Technology Used |
|--------------------|----------------|
| **Language**       | Python 3.x |
| **Face Recognition** | FaceNet (InceptionResnetV1 pretrained on VGGFace2) |
| **Hand Tracking**  | MediaPipe Hands |
| **Automation**     | PyAutoGUI |
| **Computer Vision** | OpenCV |
| **Math/Numerics**  | NumPy |
| **Data Handling**  | Torch (for embeddings) |

---

## 📸 Demo  

> *(You can add a GIF or screenshot here for better presentation.)*  

Example:  
- Face detected → Gesture control enabled  
- Pinch fingers → Zoom in/out  
- Thumb down → Volume control  
- Hand up → Cursor movement  

---

## 🔧 Installation & Setup  
### face embbiding 
-python capture_faces.py

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/henthorthayran/face-gesture-control.git
cd face-gesture-control
```
