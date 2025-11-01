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

### Step 4: Run the Application

```bash
python main.py
```

**Note**: On first run, YOLOv8 will automatically download the pre-trained model to the `models/` folder (~6MB).

## Usage

### Full-Featured Version (Recommended)

Run the main application:

```bash
python main.py
```

This uses YOLOv8 for superior object detection accuracy with color recognition and natural language descriptions.

### Lightweight Version (MobileNet SSD)

If you need faster performance on older hardware:

```bash
# First, download the MobileNet models
python utils/install_models.py

# Then run the simple version
python src/simple_vision_assistant.py
```

### Keyboard Controls

- **Q**: Quit the application
- **S**: Analyze scene and get immediate voice description

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
- "I see 3 objects. A car far away on your right, a person close on your left, one dog very close in front of you"

## Architecture

### Project Structure

```
bridging-worlds/
├── main.py                    # Main entry point
├── src/                       # Source code
│   ├── vision_assistant.py    # Full-featured version
│   └── simple_vision_assistant.py  # Lightweight version
├── models/                    # AI models (auto-downloaded)
├── utils/                     # Utility scripts
├── tests/                     # Test files
└── docs/                      # Documentation
```

See [docs/STRUCTURE.md](docs/STRUCTURE.md) for detailed structure information.

### Main Components

1. **VisionAssistant Class** (`src/vision_assistant.py`)
   - Uses YOLOv8 for state-of-the-art object detection
   - Advanced distance and position estimation
   - Sophisticated scene description generation

2. **SimpleVisionAssistant Class** (`src/simple_vision_assistant.py`)
   - Uses MobileNet SSD (lighter, faster)
   - Basic object detection with COCO classes
   - Simplified scene descriptions

3. **Text-to-Speech Module**
   - Uses Windows SAPI (win32com) for reliable TTS
   - Synchronous speech delivery for guaranteed audio playback
   - Clear, natural voice descriptions

## Detected Objects

The system can detect various objects including:
- People
- Vehicles (cars, bicycles, motorcycles, buses, trucks)
- Animals (dogs, cats, horses, birds)
- Furniture (chairs, sofas, tables)
- Electronics (TVs, laptops, phones)
- And many more...

## Customization

### Adjust Speech Rate

In `src/vision_assistant.py`, modify:

```python
self.tts_engine.Rate = 1  # Increase for faster speech (-10 to 10)
```

### Adjust Detection Confidence

In `src/vision_assistant.py`:
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
- On Windows: Uses native SAPI - should work out of the box
- Verify with: `python tests/test_tts.py`
- On Linux: Install espeak: `sudo apt-get install espeak`
- On macOS: Should work with native speech synthesis

### Slow Performance
- Use the simple version: `python src/simple_vision_assistant.py`
- Reduce camera resolution in code
- Close other applications

### Model Download Issues
- Check your internet connection
- Models are automatically saved to the `models/` directory
- Manually download and place in `models/` folder if needed

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
