AirCursor – Hand Gesture Controlled Mouse
=======================================

AirCursor is a computer vision–based application that allows users to control their mouse cursor using hand gestures captured through a webcam.
It uses MediaPipe for hand tracking and OpenCV for real-time image processing.


FEATURES
--------
- Move mouse cursor using hand movement
- Left click using gesture
- Right click using gesture
- Scroll using finger gestures
- Real-time hand landmark detection
- No additional hardware required (just a webcam)


HOW IT WORKS
------------
1. Webcam captures live video
2. MediaPipe detects hand landmarks
3. Specific finger gestures are mapped to mouse actions
4. PyAutoGUI performs system-level mouse control


TECH STACK
----------
- Python 3.9+
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy


INSTALLATION
------------
1. Clone the repository
   git clone https://github.com/Sanjay-Deshmukh/AirCursor.git
   cd AirCursor

2. Create virtual environment (recommended)
   python -m venv venv

3. Activate virtual environment (Windows)
   venv\Scripts\activate

4. Install dependencies
   pip install -r requirements.txt


RUN THE APPLICATION
-------------------
python main.py

Make sure your webcam is connected.


GESTURE CONTROLS (Example)
-------------------------
Index finger move   -> Cursor movement
Index + Thumb       -> Left click
Index + Middle      -> Right click
Ring finger up      -> Scroll down
Little finger up    -> Scroll up

(Note: Gestures may vary based on implementation)


PROJECT STRUCTURE
-----------------
AirCursor/
|
|-- main.py
|-- requirements.txt
|-- README.txt
|-- .gitignore


IMPORTANT NOTES
---------------
- Do NOT run in low-light conditions
- Keep hand within camera frame
- Works best with a plain background
- Tested on Windows OS


FUTURE IMPROVEMENTS
-------------------
- Multi-hand support
- Gesture customization
- GUI-based calibration
- Linux & macOS support


AUTHOR
------
Sanjay Deshmukh
GitHub: https://github.com/Sanjay-Deshmukh


LICENSE
-------
This project is open-source and available under the MIT License.
