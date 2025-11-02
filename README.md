# Bridging Worlds - Documentation Index

Welcome to the **Bridging Worlds** documentation! This project provides AI-powered accessibility tools for communication and environmental awareness.

## 📚 Documentation Overview

### Main Documentation
- **[README.md](../README.md)** - Project overview, installation, and quick start guide

### Feature-Specific Guides

#### 1. Sign Language Interpreter
📖 **[Sign Language Interpreter - Complete Guide](hand_keypoint_tts_usage.md)**

The most advanced feature! Real-time sign language interpretation with:
- 21-point hand keypoint detection
- Dual-hand tracking
- Text-to-Speech integration
- Interactive learning mode
- Mirror-corrected display

**Quick Start**: `python src/hand_keypoint_detection.py`

---

#### 2. AI Vision Assistant
📖 **[Vision Assistant Guide](vision_assistant_guide.md)**

Intelligent object detection and scene understanding:
- Real-time object detection (80+ classes)
- Natural language scene descriptions
- Audio feedback for accessibility
- Spatial awareness and tracking

**Quick Start**: 
- Full version: `python src/vision_assistant.py`
- Simple version: `python src/simple_vision_assistant.py`

---

## 🚀 Quick Reference

### All Available Programs

| Program | Command | Purpose |
|---------|---------|---------|
| **Sign Language Interpreter** | `python src/hand_keypoint_detection.py` | Real-time sign interpretation with TTS |
| **Vision Assistant** | `python src/vision_assistant.py` | AI object detection with scene description |
| **Simple Vision Assistant** | `python src/simple_vision_assistant.py` | Streamlined object detection |
| **ASL Alphabet Translator** | `python src/asl_translator.py` | Trained ASL alphabet recognition |
| **Basic Sign Recognition** | `python src/sign_language.py` | Simple gesture detection |

### Common Controls

| Key | Function | Used In |
|-----|----------|---------|
| **SPACE** | Next word / Advance | Sign Language Interpreter |
| **R** | Reset | Sign Language Interpreter |
| **S** | Scene description / Save | Vision Assistant / Interpreter |
| **L** | Toggle labels | Sign Language Interpreter |
| **K** | Toggle visualization | Sign Language Interpreter |
| **Q** | Quit | All programs |

---

## 🎯 Use Case Guide

### I want to...

**...interpret sign language in real-time**
→ [Sign Language Interpreter Guide](hand_keypoint_tts_usage.md)  
→ Run: `python src/hand_keypoint_detection.py`

**...learn sign language**
→ [Sign Language Interpreter - Learning Mode](hand_keypoint_tts_usage.md#learning-mode-demonstration)  
→ Use the interactive word-by-word progression feature

**...detect objects for accessibility**
→ [Vision Assistant Guide](vision_assistant_guide.md)  
→ Run: `python src/vision_assistant.py`

**...recognize ASL alphabet**
→ [README - ASL Recognition](../README.md#option-4-advanced-asl-alphabet-recognition)  
→ Train model: `python src/train_asl_model.py`  
→ Run: `python src/asl_translator.py`

---

## 🔧 Technical Documentation

### Architecture Overview

```
Bridging Worlds Platform
│
├── Sign Language Interpretation
│   ├── MediaPipe Hands (21 landmarks)
│   ├── Gesture Recognition Engine
│   ├── Text-to-Speech (Windows SAPI)
│   └── Visual Feedback System
│
├── Vision Assistance
│   ├── YOLOv8 Object Detection
│   ├── Scene Analysis Engine
│   ├── Spatial Relationship Parser
│   └── Audio Description Generator
│
└── ASL Alphabet Recognition
    ├── CNN Deep Learning Model
    ├── Real-time Inference
    ├── Confidence Scoring
    └── Translation Buffer
```

### Key Technologies

- **MediaPipe**: Hand tracking and landmark detection
- **YOLOv8**: Real-time object detection
- **PyTorch**: Deep learning framework
- **OpenCV**: Computer vision and camera handling
- **Windows SAPI**: Text-to-Speech synthesis
- **NumPy**: Numerical computations

---

## 📖 Additional Resources

### Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/jongyuldev/bridging-worlds/issues)
- **Discussions**: Join conversations in the repository
- **Contact**: Reach out to jongyuldev on GitHub

### External Learning Resources

#### Sign Language
- [Start ASL](https://www.startasl.com/) - Free ASL lessons
- [Handspeak](https://www.handspeak.com/) - ASL dictionary
- [ASL University](https://www.lifeprint.com/) - Comprehensive courses

#### Technical Skills
- [MediaPipe Documentation](https://google.github.io/mediapipe/)
- [OpenCV Python Tutorials](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Read the Code**
   - Browse `src/` for implementation details
   - Check comments and docstrings
   - Understand the architecture

2. **Try the Features**
   - Run all programs
   - Test different scenarios
   - Note what works and what doesn't

3. **Make Improvements**
   - Fix bugs
   - Add features
   - Improve documentation
   - Optimize performance

4. **Submit Changes**
   - Fork the repository
   - Create a feature branch
   - Make your changes
   - Submit a pull request

---

## 📋 Changelog

### Version 1.0 (Current)
- ✅ Sign Language Interpreter with TTS
- ✅ 21-point hand keypoint detection
- ✅ Dual-hand tracking
- ✅ AI Vision Assistant
- ✅ YOLOv8 object detection
- ✅ Mirror-corrected camera display
- ✅ Interactive learning mode
- ✅ Comprehensive documentation

### Planned Features
- 🔲 Full ASL vocabulary recognition
- 🔲 Sentence-level interpretation
- 🔲 Multi-language sign support
- 🔲 Mobile app versions
- 🔲 Cloud-based processing
- 🔲 Video call integration

---

## 📄 License

This project is open source under the MIT License. See LICENSE file for details.

---

## 👥 Credits

**Developed by**: jongyuldev  
**Repository**: [github.com/jongyuldev/bridging-worlds](https://github.com/jongyuldev/bridging-worlds)

### Acknowledgments
- MediaPipe team at Google
- YOLOv8 by Ultralytics
- PyTorch contributors
- The deaf and hard-of-hearing community
- All open source contributors

---

**Made with ❤️ to bridge communication barriers**

*Empowering communication through AI - One gesture at a time.*

---

[⬆️ Back to Top](#bridging-worlds---documentation-index)
