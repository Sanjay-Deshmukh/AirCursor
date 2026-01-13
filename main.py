# =========================================
# IMPORTS
# =========================================
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import os
import winsound
from pynput.mouse import Button, Controller

# PyInstaller splash (safe import)
try:
    import pyi_splash
except ImportError:
    pyi_splash = None

# =========================================
# GLOBAL SETTINGS
# =========================================
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

mouse = Controller()
screen_width, screen_height = pyautogui.size()

# =========================================
# SCREENSHOT FOLDER
# =========================================
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================================
# MEDIAPIPE SETUP
# =========================================
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2
)
mpDraw = mp.solutions.drawing_utils

# =========================================
# UTILITIES
# =========================================
def get_angle(a, b, c):
    return abs(np.degrees(
        np.arctan2(c[1] - b[1], c[0] - b[0]) -
        np.arctan2(a[1] - b[1], a[0] - b[0])
    ))

def finger_straight(lm, a, b, c): return get_angle(lm[a], lm[b], lm[c]) > 160
def finger_bent(lm, a, b, c): return get_angle(lm[a], lm[b], lm[c]) < 90
def distance(a, b): return np.hypot(a[0] - b[0], a[1] - b[1])

def play_shutter_sound():
    winsound.MessageBeep(winsound.MB_ICONASTERISK)

# =========================================
# GESTURES
# =========================================
def is_open_palm(lm):
    return all([
        finger_straight(lm,5,6,8),
        finger_straight(lm,9,10,12),
        finger_straight(lm,13,14,16),
        finger_straight(lm,17,18,20)
    ])

def is_fist(lm):
    return all([
        finger_bent(lm,5,6,8),
        finger_bent(lm,9,10,12),
        finger_bent(lm,13,14,16),
        finger_bent(lm,17,18,20)
    ])

def is_scroll_up(lm):
    return finger_straight(lm,5,6,8) and finger_bent(lm,9,10,12)

def is_scroll_down(lm):
    return finger_straight(lm,1,2,4) and finger_bent(lm,5,6,8)

def is_cursor_move(lm):
    return (
        finger_straight(lm,5,6,8) and
        finger_straight(lm,9,10,12) and
        finger_bent(lm,13,14,16) and
        finger_bent(lm,17,18,20)
    )

def is_left_click_pinch(lm):
    return distance(lm[4], lm[8]) < 0.04

# =========================================
# SMOOTH FAST CURSOR
# =========================================
prev_x, prev_y = screen_width // 2, screen_height // 2
alpha = 0.35
speed = 2.0

def move_cursor(lm):
    global prev_x, prev_y
    x = int(lm[8][0] * screen_width * speed)
    y = int(lm[8][1] * screen_height * speed)

    x = max(0, min(screen_width - 1, x))
    y = max(0, min(screen_height - 1, y))

    smooth_x = int(prev_x + alpha * (x - prev_x))
    smooth_y = int(prev_y + alpha * (y - prev_y))

    pyautogui.moveTo(smooth_x, smooth_y)
    prev_x, prev_y = smooth_x, smooth_y

# =========================================
# STATES
# =========================================
last_click = last_scroll = last_tab = last_screenshot = last_close = last_play_pause = 0
click_delay = 0.6
scroll_delay = 0.10
tab_delay = 1.2
screenshot_delay = 1.5
close_delay = 2.0
play_pause_delay = 1.0

# =========================================
# MAIN LOGIC
# =========================================
def detect_gesture(landmarks):
    global last_click, last_scroll, last_tab, last_screenshot, last_close, last_play_pause
    now = time.time()

    # ---------- TWO HAND GESTURES ----------
    if len(landmarks) == 2:
        lm1, lm2 = landmarks

        # ✊✊ SCREENSHOT
        if is_fist(lm1) and is_fist(lm2):
            if now - last_screenshot > screenshot_delay:
                filename = time.strftime("screenshot_%Y%m%d_%H%M%S.png")
                path = os.path.join(SCREENSHOT_DIR, filename)
                pyautogui.screenshot(path)
                play_shutter_sound()
                last_screenshot = now
            return

        # ✋✋ ALT + SHIFT + TAB
        if is_open_palm(lm1) and is_open_palm(lm2):
            if now - last_tab > tab_delay:
                pyautogui.hotkey('alt', 'shift', 'tab')
                last_tab = now
            return

        # ✋✊ CLOSE APP
        if (is_open_palm(lm1) and is_fist(lm2)) or (is_open_palm(lm2) and is_fist(lm1)):
            if now - last_close > close_delay:
                pyautogui.hotkey('alt', 'f4')
                last_close = now
            return

    # ---------- SINGLE HAND GESTURES ----------
    lm = landmarks[0]

    # ✋ PLAY / PAUSE
    if is_open_palm(lm) and now - last_play_pause > play_pause_delay:
        pyautogui.press('space')
        last_play_pause = now
        return

    if is_cursor_move(lm):
        move_cursor(lm)
        return

    if is_left_click_pinch(lm) and now - last_click > click_delay:
        mouse.click(Button.left)
        last_click = now
        return

    if is_scroll_up(lm) and now - last_scroll > scroll_delay:
        pyautogui.scroll(90)
        last_scroll = now

    elif is_scroll_down(lm) and now - last_scroll > scroll_delay:
        pyautogui.scroll(-90)
        last_scroll = now

# =========================================
# CAMERA LOOP
# =========================================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 🔥 CLOSE SPLASH SCREEN HERE
if pyi_splash:
    pyi_splash.close()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        landmarks = []
        for h in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, h, mpHands.HAND_CONNECTIONS)
            landmarks.append([(p.x, p.y) for p in h.landmark])

        detect_gesture(landmarks)

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
