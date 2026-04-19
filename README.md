# 🤟 Real-Time ASL Fingerspelling Translator
**Built for the IEEE AI & CV Camp**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![YOLOv8](https://img.shields.io/badge/Model-YOLOv8-yellow.svg)
![OpenCV](https://img.shields.io/badge/Library-OpenCV-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey.svg)

## 📌 Project Overview
This project is a real-time Computer Vision application that translates American Sign Language (ASL) alphabet gestures into text using a webcam. It utilizes a custom-trained **YOLOv8 Deep Learning model** for hand tracking and classification, wrapped in a user-friendly **Tkinter Graphical User Interface (GUI)**.

*(Upload your `locking.png` or `app_screenshot.png` to your repo, and you can show it right here!)*

## 🚀 Key Features
* **Real-Time AI Inference:** Utilizes YOLOv8 nano (`yolov8n`) to simultaneously perform bounding box regression and multi-class classification (A-Z) at high FPS.
* **Custom "Snapshot Debouncing" Logic:** Webcams inherently capture motion blur when hands move between signs, confusing standard AI models. I engineered custom Python debouncing logic that forces the model to maintain >65% confidence for 15 consecutive frames before "locking in" a translation. This eliminates flickering and double-typing!
* **Auto-Spacing & Cooldowns:** Automatically inserts spaces when the user drops their hand from the frame and features a UI cooldown timer to pace the user.
* **Export functionality:** Allows users to save their translated sentences directly to a `.txt` file.

## 🛠️ Technology Stack
* **Deep Learning:** Ultralytics YOLOv8, PyTorch
* **Computer Vision:** OpenCV (`cv2`)
* **Interface:** Tkinter, Pillow (PIL)
* **Training:** Google Colab (Tesla T4 GPU), Roboflow (Data Management)

## ⚙️ How to Run Locally

1. **Clone this repository:**
   ```bash
   git clone https://github.com/OmarBahaa1/ASL-RealTime-Translator.git
   cd ASL-RealTime-Translator
2. **Install the required dependencies:**
      ```bash
      pip install ultralytics opencv-python Pillow

3. **Run the application: Make sure you have a webcam connected, then run:**
      ```bash
      python translator.py


## 📊 Model Performance

The model was trained for 100 epochs on a custom dataset of 600+ augmented ASL images.

* **mAP50:** 96.2%
* **Precision:** 92.8%
* **Recall:** 88.7%

---

## 🔮 Future Work

Currently, this model is an *ASL Fingerspelling Translator* (spatial classification). Future iterations will implement **Google MediaPipe** for skeletal keypoint extraction and **LSTM Recurrent Neural Networks** to understand dynamic, temporal sign language movements (full words and sentences).




