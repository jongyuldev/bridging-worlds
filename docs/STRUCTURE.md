# Project Structure

```
bridging-worlds/
│
├── main.py                          # Main entry point - run this file
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
│
├── src/                            # Source code
│   ├── vision_assistant.py         # Main vision assistant (YOLO-based)
│   ├── simple_vision_assistant.py  # Lightweight version (MobileNet)
│   ├── sign.py                     # Additional feature
│   └── sign_pong.py               # Additional feature
│
├── models/                         # AI models
│   ├── yolov8n.pt                 # YOLO model (auto-downloaded)
│   └── MobileNetSSD_deploy.*      # MobileNet models (if using simple version)
│
├── utils/                          # Utility scripts
│   └── install_models.py          # Script to download required models
│
├── tests/                          # Test files
│   └── test_tts.py                # TTS testing script
│
├── docs/                           # Documentation
│   └── IMPROVEMENTS.md            # Feature improvements log
│
└── .venv/                          # Virtual environment (not in git)
```

## How to Use

### Quick Start
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run the main application
python main.py
```

### File Descriptions

#### Main Files
- **main.py** - Primary entry point for the application
- **requirements.txt** - List of Python package dependencies

#### Source Code (src/)
- **vision_assistant.py** - Full-featured version with YOLO object detection, color recognition, and natural language descriptions
- **simple_vision_assistant.py** - Lightweight alternative using MobileNet SSD
- **sign.py** & **sign_pong.py** - Additional experimental features

#### Models (models/)
- Contains AI model files
- YOLO models are automatically downloaded here
- MobileNet models can be installed using utils/install_models.py

#### Utilities (utils/)
- **install_models.py** - Downloads MobileNet SSD models for the simple version

#### Tests (tests/)
- **test_tts.py** - Verify text-to-speech functionality

#### Documentation (docs/)
- **IMPROVEMENTS.md** - Changelog of feature improvements

## Running Different Versions

### Main Vision Assistant (Recommended)
```bash
python main.py
```

### Simple Version
```bash
python src/simple_vision_assistant.py
```

### Test TTS
```bash
python tests/test_tts.py
```

## Development Notes

- All source code is in the `src/` directory
- Models are stored in `models/` directory
- Keep the root directory clean with only entry points
- Documentation goes in `docs/`
- Test files go in `tests/`
