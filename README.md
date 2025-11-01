# Bridging Worlds - Vision Assistant for the Blind

A computer vision application that helps blind and visually impaired people understand their surroundings using real-time object detection and text-to-speech feedback.

## Features

- **Real-time Object Detection**: Uses advanced AI models (YOLO or MobileNet SSD) to detect objects in the environment
- **Text-to-Speech Feedback**: Provides audio descriptions of detected objects and their positions
- **Distance Estimation**: Estimates relative distances of detected objects (close, medium, far)
- **Spatial Awareness**: Indicates whether objects are on the left, right, or in front of the user
- **Automatic Announcements**: Periodically announces the scene description (every 5 seconds by default)
- **On-Demand Descriptions**: Press 's' to get an immediate scene description
- **Multiple Implementations**: Choose between a full-featured version (YOLO) or a lightweight version (MobileNet SSD)

## Installation

### Prerequisites

- Python 3.8 or higher
- Webcam
- Windows/Linux/macOS

### Step 1: Clone the Repository

```bash
git clone https://github.com/jongyuldev/bridging-worlds.git
cd bridging-worlds
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Linux/Mac
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Models (for Simple Version)

If using the simple version with MobileNet SSD:

```bash
python install_models.py
```

## Usage

### Full-Featured Version (YOLO)

This version uses YOLOv8 for superior object detection accuracy:

```bash
python vision_assistant.py
```

**Note**: On first run, YOLOv8 will automatically download the pre-trained model (~6MB).

### Lightweight Version (MobileNet SSD)

This version is faster and uses less resources:

```bash
python simple_vision_assistant.py
```

### Keyboard Controls

- **Q**: Quit the application
- **S**: Get immediate scene description
- **H**: Get help (full version only)

## How It Works

1. **Video Capture**: The application captures video from your webcam in real-time
2. **Object Detection**: AI models analyze each frame to detect common objects (people, cars, animals, furniture, etc.)
3. **Scene Analysis**: The system analyzes:
   - What objects are present
   - How many of each object
   - Where they are located (left, right, center)
   - Estimated distance (close, medium, far)
4. **Audio Feedback**: Natural language descriptions are converted to speech using text-to-speech
5. **Continuous Monitoring**: The system continuously monitors the environment and provides updates

## Example Output

The assistant might say things like:
- "I see one person at medium distance in front of you"
- "I see 3 objects. A car far away on your right, a person close on your left"
- "One dog very close in front of you"

## Architecture

### Main Components

1. **VisionAssistant Class** (`vision_assistant.py`)
   - Uses YOLOv8 for state-of-the-art object detection
   - Advanced distance and position estimation
   - Sophisticated scene description generation

2. **SimpleVisionAssistant Class** (`simple_vision_assistant.py`)
   - Uses MobileNet SSD (lighter, faster)
   - Basic object detection with COCO classes
   - Simplified scene descriptions

3. **Text-to-Speech Module**
   - Uses pyttsx3 for cross-platform TTS
   - Non-blocking speech queue system
   - Adjustable speech rate and volume

## Detected Objects

The system can detect various objects including:
- People
- Vehicles (cars, bicycles, motorcycles, buses, trucks)
- Animals (dogs, cats, horses, birds)
- Furniture (chairs, sofas, tables)
- Electronics (TVs, laptops, phones)
- And many more...

## Customization

### Adjust Announcement Interval

In `vision_assistant.py` or `simple_vision_assistant.py`, modify:

```python
self.announcement_interval = 5  # Change to desired seconds
```

### Adjust Speech Rate

```python
self.tts_engine.setProperty('rate', 150)  # Increase for faster speech
```

### Adjust Detection Confidence

In `vision_assistant.py`:
```python
results = self.model(frame, conf=0.5, verbose=False)  # Change conf value
```

## System Requirements

### Minimum Requirements
- CPU: Dual-core processor
- RAM: 4GB
- Webcam: 640x480 resolution
- OS: Windows 10/11, Ubuntu 18.04+, macOS 10.14+

### Recommended Requirements
- CPU: Quad-core processor
- RAM: 8GB
- Webcam: 1080p
- GPU: Optional but improves performance (CUDA-compatible)

## Troubleshooting

### "Could not open webcam" Error
- Ensure your webcam is connected and not in use by another application
- Try changing the camera index in code: `cv2.VideoCapture(1)` instead of `0`

### TTS Not Working
- On Windows: Should work out of the box
- On Linux: Install espeak: `sudo apt-get install espeak`
- On macOS: Should work with native speech synthesis

### Slow Performance
- Use the simple version: `simple_vision_assistant.py`
- Reduce camera resolution in code
- Close other applications

### Model Download Issues
- Check your internet connection
- Manually download models and place in the correct directories

## Future Enhancements

Potential improvements:
- [ ] Distance measurement using depth cameras
- [ ] Face recognition for familiar people
- [ ] Obstacle warning system
- [ ] Indoor navigation assistance
- [ ] Text reading (OCR) for signs and labels
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Cloud-based processing option
- [ ] Haptic feedback integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- YOLOv8 by Ultralytics
- OpenCV community
- pyttsx3 developers
- MobileNet SSD by chuanqi305

## Contact

For questions or suggestions, please open an issue on GitHub.

## Disclaimer

This application is designed to assist visually impaired users but should not be relied upon as the sole means of navigation or safety. Always use additional assistive devices and techniques as recommended by professionals.

---

**Made with ❤️ to help bridge the gap between vision and understanding**
