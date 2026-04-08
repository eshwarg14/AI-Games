# 🎮 Gesture Controlled Maze Runner

A real-time maze game controlled using hand gestures via webcam. Built using MediaPipe and OpenCV, this project allows players to navigate a maze using intuitive hand movements.

---

## Preview

![Demo](https://github.com/eshwarg14/AI-Games/raw/e47a2ea863a8cc61de45a0c92bbfd0313af64eb9/Images/MR.png)

---

## ✨ Features

- ✋ Control player using hand gestures  
- 🎮 Real-time movement with webcam input  
- 🧠 Gesture recognition (Thumbs Up, Fist, Peace, Open Palm)  
- 🧱 Randomly generated maze  
- 🎯 Reach the exit to score points  
- 🔄 Automatic maze reset after win  
- 📊 Live score tracking  
- 🖥️ Clean UI with camera feed  

---

## 🧠 Technologies Used

```
opencv-python
mediapipe
numpy
pillow
tkinter
```

📦 Install dependencies:

```bash
pip install opencv-python mediapipe numpy pillow
```

---

## ▶️ Usage

```bash
python main.py
```

Press `Q` or close the window to exit.

---

## ✋ Controls & Gestures

| Gesture | Action |
|--------|--------|
| 👍 Thumbs Up | Move Up |
| ✊ Fist | Move Down |
| ✌️ Peace Sign | Move Left |
| 🖐️ Open Palm | Move Right |

---

## 🛠️ How It Works

- 🤖 **Hand Tracking** – MediaPipe detects hand landmarks  
- ✋ **Gesture Recognition** – Finger positions determine gesture  
- 🎮 **Movement System** – Player moves based on gesture input  
- 🧱 **Maze System** – Random obstacles and exit generation  
- 📷 **Live Feed** – Webcam feed processed in real-time  

---

## 📁 Project Structure

```
├── main.py        # Main game logic
└── README.md
```

---

## ⚠️ Requirements

- 📷 Webcam (mandatory)  
- 🐍 Python 3.8+  
- 💡 Good lighting for accurate gesture detection  

---

## 👨‍💻 Author

**Eshwar G & Shivani R**

---

## 📄 License

This project is licensed under the MIT License.
