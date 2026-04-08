import tkinter as tk
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import threading
import time
import random

GRID = 12
CELL = 50
PAD = 20
CAM_W, CAM_H = 240, 180

GESTURES = {"Thumbs Up": "UP", "Peace Sign": "LEFT", "Open Palm": "RIGHT", "Fist": "DOWN"}
MOVES = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

class MazeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Maze Runner with Hand Gestures")
        self.root.config(bg="white")
        self.running = True
        self.last_move = 0
        self.move_delay = 0.35
        self.score = 0
        self.won = False

        W = GRID * CELL + PAD * 2
        H = GRID * CELL + PAD * 2
        SIDE_W = CAM_W + PAD * 2
        self.root.geometry(f"{W + SIDE_W}x{H + 40}")

        self.canvas = tk.Canvas(self.root, width=W, height=H, bg="white", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        side = tk.Frame(self.root, bg="white", width=SIDE_W)
        side.place(x=W, y=0, width=SIDE_W, height=H + 40)

        self.cam_label = tk.Label(side, bg="white", bd=2, relief="groove")
        self.cam_label.pack(padx=PAD, pady=(PAD, 6))

        self.score_var = tk.StringVar(value="Score: 0")
        tk.Label(side, textvariable=self.score_var, font=("Arial", 16, "bold"),
                 fg="#2196F3", bg="white").pack()

        self.gesture_var = tk.StringVar(value="Gesture: None")
        tk.Label(side, textvariable=self.gesture_var, font=("Arial", 11),
                 fg="#555555", bg="white").pack(pady=2)

        self.status_var = tk.StringVar(value="Reach the exit!")
        self.status_label = tk.Label(side, textvariable=self.status_var, font=("Arial", 12, "bold"),
                                     fg="green", bg="white", wraplength=CAM_W)
        self.status_label.pack(pady=4)

        hint = "Thumbs Up = Up\nFist = Down\nPeace Sign = Left\nOpen Palm = Right"
        tk.Label(side, text=hint, font=("Arial", 10), fg="#888888", bg="white", justify="left").pack(pady=6)

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.cap = cv2.VideoCapture(0)

        self.reset_maze()
        threading.Thread(target=self.cam_loop, daemon=True).start()
        self.update_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def reset_maze(self):
        self.won = False
        self.maze = [["." for _ in range(GRID)] for _ in range(GRID)]
        for _ in range(GRID * 2):
            r, c = random.randrange(GRID), random.randrange(GRID)
            if (r, c) not in ((0, 0), (0, 1), (1, 0)):
                self.maze[r][c] = "X"
        while True:
            er, ec = random.randrange(GRID), random.randrange(GRID)
            if self.maze[er][ec] == "." and (er, ec) != (0, 0):
                self.maze[er][ec] = "E"
                break
        self.pos = [0, 0]
        self.status_var.set("Reach the exit!")
        self.status_label.config(fg="green")

    def draw_maze(self):
        self.canvas.delete("all")
        for r in range(GRID):
            for c in range(GRID):
                x0 = PAD + c * CELL
                y0 = PAD + r * CELL
                cell = self.maze[r][c]
                fill = "black" if cell == "X" else "green" if cell == "E" else "white"
                self.canvas.create_rectangle(x0, y0, x0 + CELL, y0 + CELL,
                                             fill=fill, outline="gray", width=1)

        pr, pc = self.pos
        x0 = PAD + pc * CELL + CELL * 0.1
        y0 = PAD + pr * CELL + CELL * 0.1
        self.canvas.create_oval(x0, y0, x0 + CELL * 0.8, y0 + CELL * 0.8,
                                fill="blue", outline="#003399", width=2)

        if self.won:
            cx = GRID * CELL // 2 + PAD
            cy = GRID * CELL // 2 + PAD
            self.canvas.create_rectangle(cx - 160, cy - 55, cx + 160, cy + 55,
                                         fill="#e8f5e9", outline="green", width=3)
            self.canvas.create_text(cx, cy - 20, text="You reached the exit!",
                                    font=("Arial", 20, "bold"), fill="green")
            self.canvas.create_text(cx, cy + 18, text=f"Score: {self.score}  (+1 point)",
                                    font=("Arial", 14), fill="#2196F3")

    def recognize(self, lm):
        open_f = [lm[4].x < lm[3].x] + [lm[t].y < lm[p].y for t, p in zip([8, 12, 16, 20], [6, 10, 14, 18])]
        n = sum(open_f)
        if n == 1 and open_f[0]: return "Thumbs Up"
        if n == 2 and open_f[1] and open_f[2]: return "Peace Sign"
        if n == 5: return "Open Palm"
        if n == 0: return "Fist"
        return None

    def move_player(self, gesture):
        if self.won:
            return
        now = time.time()
        if now - self.last_move < self.move_delay:
            return
        direction = GESTURES.get(gesture)
        if not direction:
            return
        dr, dc = MOVES[direction]
        nr, nc = self.pos[0] + dr, self.pos[1] + dc
        if 0 <= nr < GRID and 0 <= nc < GRID and self.maze[nr][nc] != "X":
            self.pos = [nr, nc]
            self.last_move = now
            if self.maze[nr][nc] == "E":
                self.won = True
                self.score += 1
                self.score_var.set(f"Score: {self.score}")
                self.status_var.set(f"Next maze loading...")
                self.status_label.config(fg="orange")
                self.root.after(2200, self.reset_maze)

    def cam_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.03)
                continue
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = self.hands.process(rgb)
            gesture = None
            if res.multi_hand_landmarks:
                lm = res.multi_hand_landmarks[0].landmark
                gesture = self.recognize(lm)
                self.mp_draw.draw_landmarks(frame, res.multi_hand_landmarks[0], self.mp_hands.HAND_CONNECTIONS)
            self.gesture_var.set(f"Gesture: {gesture or 'None'}")
            if gesture:
                self.move_player(gesture)
            small = cv2.resize(frame, (CAM_W, CAM_H))
            img = Image.fromarray(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.cam_label.config(image=imgtk)
            self.cam_label.image = imgtk
            time.sleep(0.03)

    def update_ui(self):
        self.draw_maze()
        if self.running:
            self.root.after(80, self.update_ui)

    def close(self):
        self.running = False
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    MazeGame()
