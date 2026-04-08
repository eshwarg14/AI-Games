import streamlit as st
import cv2
import mediapipe as mp
import random
import time
from collections import deque
from PIL import Image
import numpy as np
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

st.set_page_config(page_title="Rock Paper Scissors", layout="wide")
st.title("✋ Rock Paper Scissors – Human vs AI")

IMG_PATHS = {
    "Rock": r"Rock.png",
    "Paper": r"Paper.png",
    "Scissors": r"Scissors.png",
    "NoHand": r"Blank.jpeg"
}
MOVE_IMAGES = {k: Image.open(v).resize((150, 150)) for k, v in IMG_PATHS.items()}


def fingers_up(hand_landmarks, handedness_str):
    lm = hand_landmarks.landmark
    TIP_IDS = [4, 8, 12, 16, 20]
    PIP_IDS = [2, 6, 10, 14, 18]
    fingers = []
    tip_x, ip_x = lm[TIP_IDS[0]].x, lm[PIP_IDS[0]].x
    if handedness_str == "Right":
        fingers.append(tip_x < ip_x)
    else:
        fingers.append(tip_x > ip_x)
    for i in range(1, 5):
        fingers.append(lm[TIP_IDS[i]].y < lm[PIP_IDS[i]].y)
    return fingers

def classify_rps(fingers):
    thumb, idx, mid, ring, pinky = fingers
    if all(fingers): return "Paper"
    if not any(fingers): return "Rock"
    if idx and mid and not ring and not pinky: return "Scissors"
    return "Unknown"

def decide_winner(user_move, ai_move):
    if user_move == ai_move:
        return "Tie"
    wins = {("Rock", "Scissors"), ("Paper", "Rock"), ("Scissors", "Paper")}
    return "User" if (user_move, ai_move) in wins else "AI"

if "user_score" not in st.session_state:
    st.session_state.user_score = 0
    st.session_state.ai_score = 0
    st.session_state.last_user_move = "NoHand"
    st.session_state.last_ai_move = "NoHand"
    st.session_state.last_result = ""
    st.session_state.recent_gestures = deque(maxlen=12)
    st.session_state.freeze_until = 0

col1, col2, col3 = st.columns([2, 1, 1])
cam_placeholder = col1.empty()
user_placeholder = col2.empty()
ai_placeholder = col3.empty()
result_placeholder = st.empty()

cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.5, max_num_hands=1)

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Cannot access webcam.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    gesture = "NoHand"

    if results.multi_hand_landmarks and results.multi_handedness:
        hand_landmarks = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0].classification[0].label
        fingers = fingers_up(hand_landmarks, handedness)
        gesture = classify_rps(fingers)
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        st.session_state.recent_gestures.append(gesture)
    else:
        st.session_state.recent_gestures.append("NoHand")

    stable_gesture = None
    if len(st.session_state.recent_gestures) >= 12:
        last = list(st.session_state.recent_gestures)[-12:]
        if all(x == last[0] for x in last) and last[0] in ("Rock", "Paper", "Scissors"):
            stable_gesture = last[0]

    now = time.time()
    if stable_gesture and now > st.session_state.freeze_until:
        st.session_state.freeze_until = now + 4
        user_move = stable_gesture
        ai_move = random.choice(["Rock", "Paper", "Scissors"])
        winner = decide_winner(user_move, ai_move)

        st.session_state.last_user_move = user_move
        st.session_state.last_ai_move = ai_move
        st.session_state.last_result = (
            "You WIN! 🎉" if winner == "User" else
            "AI Wins! 🤖" if winner == "AI" else
            "Tie! 😐"
        )
        if winner == "User":
            st.session_state.user_score += 1
        elif winner == "AI":
            st.session_state.ai_score += 1
        st.session_state.recent_gestures.clear()

    cam_placeholder.image(frame, channels="BGR")
    user_placeholder.image(MOVE_IMAGES[st.session_state.last_user_move],
                           caption=f"You ({st.session_state.user_score})")
    ai_placeholder.image(MOVE_IMAGES[st.session_state.last_ai_move],
                         caption=f"AI ({st.session_state.ai_score})")
    result_placeholder.markdown(f"## {st.session_state.last_result}")

    time.sleep(0.03)  
