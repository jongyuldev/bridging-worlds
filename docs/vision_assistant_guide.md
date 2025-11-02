# AI Vision Assistant - User Guide

## Overview

The **Bridging Worlds AI Vision Assistant** is an intelligent accessibility tool that provides real-time object detection, scene understanding, and audio descriptions for users with visual impairments or anyone needing environmental awareness.

## Features

### Core Capabilities
- **Real-time Object Detection**: YOLOv8-powered recognition of 80+ object classes
- **Scene Description**: Natural language descriptions of your environment
- **Spatial Awareness**: Position and distance estimation for detected objects
- **Audio Feedback**: Text-to-Speech announcements for hands-free operation
- **Multi-Object Tracking**: Simultaneous detection and tracking

### Visual Display
- **Bounding Boxes**: Color-coded object detection boxes
- **Confidence Scores**: Real-time accuracy indicators
- **Object Labels**: Clear text identification
- **Mirror-Corrected**: Natural, intuitive camera view

## Quick Start

### Launch the Assistant

```bash
python src/vision_assistant.py
```

### Controls

| Key | Function |
|-----|----------|
| **S** | Get detailed scene description |
| **Q** | Quit the application |

## Use Cases

### Accessibility
- 🦯 **Navigation Aid**: Environmental awareness for visually impaired users
- 🚶 **Obstacle Detection**: Identify objects in path
- 🏠 **Home Navigation**: Find items and navigate rooms
- 🛍️ **Shopping Assistance**: Identify products and items

### Safety
- 🚗 **Traffic Awareness**: Detect vehicles and pedestrians
- ⚠️ **Hazard Detection**: Identify potential dangers
- 🚪 **Exit Identification**: Locate doors and exits

### General Use
- 🔍 **Item Finding**: Locate specific objects
- 📦 **Inventory**: Count and identify items
- 🎥 **Monitoring**: Keep track of spaces
- 📚 **Organization**: Identify and categorize objects

## Technical Details

### Object Detection
- **Model**: YOLOv8n (nano) - optimized for speed
- **Classes**: 80 COCO dataset objects
- **Performance**: 30+ FPS real-time detection
- **Accuracy**: High confidence thresholds

### COCO Object Classes
People, vehicles, animals, furniture, electronics, kitchen items, sports equipment, and more including:
- person, bicycle, car, motorcycle, airplane, bus, train, truck, boat
- traffic light, fire hydrant, stop sign, parking meter, bench
- cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe
- backpack, umbrella, handbag, tie, suitcase, frisbee, skis
- bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple
- chair, couch, potted plant, bed, dining table, toilet, tv, laptop
- And many more...

## Simple Vision Assistant

For a streamlined experience, use the simple version:

```bash
python src/simple_vision_assistant.py
```

### Features
- **Auto-Announce**: Automatic periodic scene descriptions
- **Simplified Interface**: Easier for beginners
- **Lower Resource Usage**: Optimized performance
- **Quick Setup**: Minimal configuration required

### Controls
| Key | Function |
|-----|----------|
| **S** | Force scene description |
| **Q** | Quit the application |

## System Requirements

- Python 3.8+
- Webcam (720p or higher)
- 4GB RAM minimum
- Windows/Linux/macOS
- Good lighting conditions

## Installation

```bash
# Install dependencies
pip install opencv-python ultralytics numpy pywin32

# Run vision assistant
python src/vision_assistant.py

# Or run simple version
python src/simple_vision_assistant.py
```

## Troubleshooting

### Camera Issues
- Ensure no other apps are using the camera
- Check camera permissions
- Try different camera index if multiple cameras

### Detection Issues
- Improve lighting conditions
- Ensure objects are clearly visible
- Move camera closer to objects
- Reduce background clutter

### Audio Issues
- Check system volume
- Verify TTS is working
- On Windows: Ensure SAPI is enabled
- Test with `tests/test_tts.py`

## Privacy & Safety

- ✅ All processing is local (no cloud)
- ✅ No video recording or storage
- ✅ Camera active only when app runs
- ✅ No data transmission

---

**Part of the Bridging Worlds accessibility platform**

[← Back to Main Documentation](../README.md)
