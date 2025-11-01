# Sign Language Interpreter Guide

## Overview

The Sign Language Interpreter uses **keypoint detection** with MediaPipe to recognize hand gestures and interpret sign language in real-time. This tool helps bridge communication between people who can and cannot use sign language.

## Features

### 🎯 Core Capabilities

- **Real-time Hand Detection**: Detects up to 2 hands simultaneously with 21 keypoints per hand
- **Gesture Recognition**: Recognizes common signs and gestures including:
  - Numbers 0-5
  - Thumbs up/down (Yes/No)
  - OK sign
  - Peace/Victory sign
  - Directional pointing
  - ASL "I Love You"
  - And more...

- **Gesture Smoothing**: Uses a buffer system to avoid false positives
- **Translation History**: Keeps track of recognized gestures in sequence
- **Visual Feedback**: Real-time display of:
  - Hand landmarks and connections
  - Current gesture with confidence level
  - Translation sequence
  - Hand labels (Left/Right)

### 🔍 How It Works

1. **Keypoint Detection**: MediaPipe detects 21 keypoints on each hand:
   - Wrist (0)
   - Thumb: CMC (1), MCP (2), IP (3), Tip (4)
   - Index: MCP (5), PIP (6), DIP (7), Tip (8)
   - Middle: MCP (9), PIP (10), DIP (11), Tip (12)
   - Ring: MCP (13), PIP (14), DIP (15), Tip (16)
   - Pinky: MCP (17), PIP (18), DIP (19), Tip (20)

2. **Feature Extraction**: Analyzes keypoint relationships:
   - Finger extension states
   - Distance between keypoints
   - Angles between joints
   - Spatial positions relative to wrist

3. **Gesture Classification**: Recognizes gestures based on:
   - Number of extended fingers
   - Finger combinations
   - Hand orientation
   - Relative positions

4. **Temporal Smoothing**: Requires gestures to be held for 1 second before adding to translation to ensure accuracy

## Usage

### Basic Usage

```bash
# Activate virtual environment
source my_project_env/bin/activate  # macOS/Linux
# or
my_project_env\Scripts\activate  # Windows

# Run the interpreter
python src/sign.py
```

### Keyboard Controls

- **'q'**: Quit the application
- **'c'**: Clear translation history

### Tips for Best Results

1. **Lighting**: Ensure good, even lighting on your hands
2. **Background**: Use a plain, contrasting background
3. **Distance**: Keep hands at a comfortable distance from the camera (30-60cm)
4. **Movement**: Hold gestures steady for 1 second for recognition
5. **Camera Position**: Position camera at chest level for natural signing

## Recognized Gestures

### Numbers
- **0**: Fist (all fingers closed)
- **1**: Index finger extended
- **2**: Index and middle fingers extended
- **3**: Thumb, index, and middle fingers extended
- **4**: All fingers except thumb extended
- **5**: All fingers extended (open palm)

### Common Signs
- **👍 Thumbs Up**: Only thumb extended, pointing up → "Good/Yes"
- **👎 Thumbs Down**: Only thumb extended, pointing down → "Bad/No"
- **👌 OK**: Thumb and index forming a circle → "OK/Perfect"
- **✌️ Peace**: Index and middle fingers spread → "Peace/Victory/2"
- **🤟 I Love You**: Thumb, index, and pinky extended (ASL)
- **🤘 Rock On**: Index and pinky extended (no thumb)

### Directional
- **👈 Pointing Left**: Index finger pointing left
- **👉 Pointing Right**: Index finger pointing right
- **👆 Pointing Up**: Index finger pointing up
- **👇 Pointing Down**: Index finger pointing down

### Greetings
- **✋ Hello/Stop**: Open palm, all 5 fingers extended
- **✊ Fist**: Closed fist (also letter 'S' in ASL)

## Advanced Customization

### Adjust Sensitivity

You can customize the interpreter by modifying initialization parameters:

```python
from src.sign import SignLanguageInterpreter

interpreter = SignLanguageInterpreter(
    min_detection_confidence=0.7,  # Higher = more selective
    min_tracking_confidence=0.5,   # Higher = less jitter
    gesture_buffer_size=10         # Larger = more smoothing
)

interpreter.run(camera_index=0)
```

### Parameters Explained

- **min_detection_confidence** (0.0-1.0): Minimum confidence for initial hand detection
  - Lower values: More sensitive, may detect false positives
  - Higher values: More selective, may miss some hands
  
- **min_tracking_confidence** (0.0-1.0): Minimum confidence for hand tracking
  - Lower values: Tracks hands even with poor visibility
  - Higher values: More stable tracking but may lose hands
  
- **gesture_buffer_size** (int): Number of frames to smooth gesture recognition
  - Smaller values: Faster response, less stable
  - Larger values: More stable, slower response

- **gesture_hold_time** (seconds): Time to hold gesture before adding to translation
  - Default: 1.0 seconds
  - Adjust in code: `interpreter.gesture_hold_time = 1.5`

## Integration Examples

### Use in Your Own Project

```python
from src.sign import SignLanguageInterpreter

# Create interpreter
interpreter = SignLanguageInterpreter()

# Process a single frame
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Detect hands
image, results = interpreter.detect_hands(frame)

# Recognize gesture if hands detected
if results.multi_hand_landmarks:
    for hand_landmarks, handedness in zip(
        results.multi_hand_landmarks, 
        results.multi_handedness
    ):
        hand_label = handedness.classification[0].label
        gesture = interpreter.recognize_gesture(hand_landmarks, hand_label)
        print(f"{hand_label} hand: {gesture}")
```

### Add Text-to-Speech

You can extend the interpreter to speak recognized gestures:

```python
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# In your main loop, after gesture recognition:
if new_gesture_recognized:
    engine.say(gesture_text)
    engine.runAndWait()
```

## Technical Details

### Performance

- **FPS**: 20-30 fps on typical webcams
- **Latency**: ~50-100ms detection latency
- **Hands**: Supports up to 2 hands simultaneously

### Requirements

- **Python**: 3.8+
- **Dependencies**:
  - opencv-python (cv2)
  - mediapipe
  - numpy

### MediaPipe Hand Landmark Model

The system uses MediaPipe's hand landmark detection model which:
- Detects 21 3D hand keypoints
- Works in real-time (30+ fps)
- Handles occlusions and varying lighting
- Provides palm detection and hand tracking

## Troubleshooting

### Low FPS
- Reduce camera resolution
- Close other applications
- Reduce `max_num_hands` to 1

### Inaccurate Detection
- Improve lighting conditions
- Use a contrasting background
- Keep hands in frame
- Increase `min_detection_confidence`

### Jittery Landmarks
- Increase `min_tracking_confidence`
- Increase `gesture_buffer_size`

### Camera Not Opening
```bash
# Check camera permissions
# macOS: System Preferences → Security & Privacy → Camera
# Allow access for Terminal/IDE

# Try different camera index
interpreter.run(camera_index=1)  # or 2, 3, etc.
```

## Future Enhancements

Potential improvements for the sign language interpreter:

1. **Extended ASL Alphabet**: Full A-Z fingerspelling recognition
2. **Machine Learning**: Train custom model for more complex signs
3. **Sentence Construction**: Grammar and sentence structure
4. **Two-Way Communication**: Add text-to-sign animation
5. **Multi-Language**: Support for different sign languages (ASL, BSL, etc.)
6. **Context Awareness**: Use previous gestures to improve accuracy
7. **Mobile App**: Deploy on smartphones/tablets

## Contributing

To add new gestures:

1. Study the keypoint relationships in `recognize_gesture()` method
2. Define new gesture patterns based on:
   - Extended finger combinations
   - Keypoint distances
   - Joint angles
   - Hand orientation
3. Add gesture recognition logic
4. Test thoroughly with various hand sizes and positions

## License

Part of the Bridging Worlds project - helping people communicate across barriers.

---

**Made with ❤️ to bridge communication gaps**
