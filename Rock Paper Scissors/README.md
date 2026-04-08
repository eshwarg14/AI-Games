# ✋ Rock Paper Scissors - Human vs AI

A real-time Rock Paper Scissors game using hand gestures via webcam. Built with Streamlit, OpenCV, and MediaPipe, this app allows users to play against an AI using hand movements.

---

## Preview

![Demo](https://github.com/eshwarg14/AI-Games/raw/5479f9d2f5cd6c8b86da7960012a32ccb61ca93b/Images/R.png)
![Demo](https://github.com/eshwarg14/AI-Games/raw/5479f9d2f5cd6c8b86da7960012a32ccb61ca93b/Images/P.png)
![Demo](https://github.com/eshwarg14/AI-Games/raw/5479f9d2f5cd6c8b86da7960012a32ccb61ca93b/Images/S.png)

---

## ✨ Features

- ✋ Gesture-based gameplay (Rock, Paper, Scissors)  
- 🤖 Play against AI opponent  
- 📷 Real-time webcam detection  
- 🧠 Stable gesture detection (reduces flicker)  
- 🎯 Score tracking (User vs AI)  
- 🖥️ Interactive UI using Streamlit  

---

## 🧠 What is Streamlit?

**Streamlit** is a Python framework used to build interactive web applications easily.

- 🌐 Converts Python scripts into web apps  
- ⚡ No frontend (HTML/CSS/JS) required  
- 📊 Ideal for AI, ML, and data science projects  
- 🖥️ Runs in browser (localhost)

👉 In this project, Streamlit is used to:
- Display webcam feed  
- Show game UI (scores, moves, result)  
- Create interactive layout  

---

## 🧠 Technologies Used

```
streamlit
opencv-python
mediapipe
numpy
pillow
```

📦 Install dependencies:

```bash
pip install streamlit opencv-python mediapipe numpy pillow
```

---

## ▶️ How to Run

```bash
streamlit run main.py
```

👉 Then open the browser link shown (usually `http://localhost:8501`)

---

## 📁 Project Structure

```
├── main.py            # Main application
├── utilities/         # Images used in game
│   ├── Rock.png
│   ├── Paper.png
│   ├── Scissors.png
│   └── Blank.jpeg
└── README.md
```

---

## 🛠️ How It Works

- 📷 Webcam captures live video  
- 🤖 MediaPipe detects hand landmarks  
- ✋ Finger positions determine gesture  
- 🧠 Gesture is stabilized over multiple frames  
- 🎮 AI randomly selects move  
- 🏆 Winner is decided based on rules  
- 📊 Scores are updated in real-time  

---

## ⚠️ Important Notes

- 📷 Webcam required  
- 🐍 Python 3.8+  
- 💡 Good lighting improves accuracy  

---

## 🔧 Important Setup

Update image paths in your code:

```python
IMG_PATHS = {
    "Rock": "utilities/Rock.png",
    "Paper": "utilities/Paper.png",
    "Scissors": "utilities/Scissors.png",
    "NoHand": "utilities/Blank.jpeg"
}
```

---

## 👨‍💻 Authors

**Eshwar G & Shivani R**

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you like this project:

- ⭐ Star the repo  
- 🍴 Fork it  
- 🛠️ Contribute  

