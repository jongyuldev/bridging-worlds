# Sign Language Interpreter - Quick Reference Card

## 🚀 Quick Start
```bash
python src/sign.py
```

## ⌨️ Controls
| Key | Action |
|-----|--------|
| `q` | Quit application |
| `c` | Clear translation history |

## 🤟 Recognized Gestures

### Numbers (0-5)
| Gesture | Sign Description |
|---------|------------------|
| **0** | ✊ Closed fist (all fingers down) |
| **1** | ☝️ Index finger up |
| **2** | ✌️ Index + middle fingers up |
| **3** | 🤞 Thumb + index + middle up |
| **4** | 🖐️ All except thumb |
| **5** | ✋ All fingers extended |

### Common Signs
| Gesture | Sign Description | Meaning |
|---------|------------------|---------|
| 👍 **Thumbs Up** | Only thumb extended, pointing up | Yes / Good / Agree |
| 👎 **Thumbs Down** | Only thumb extended, pointing down | No / Bad / Disagree |
| 👌 **OK** | Thumb + index form circle | OK / Perfect |
| ✌️ **Peace** | Index + middle spread apart | Peace / Victory / 2 |
| 🤟 **ILY** | Thumb + index + pinky up | I Love You (ASL) |
| 🤘 **Rock** | Index + pinky up (no thumb) | Rock On |

### Directional
| Gesture | Sign Description |
|---------|------------------|
| 👈 **Left** | Index pointing left |
| 👉 **Right** | Index pointing right |
| 👆 **Up** | Index pointing up |
| 👇 **Down** | Index pointing down |

### Other
| Gesture | Sign Description | Meaning |
|---------|------------------|---------|
| ✊ **Fist** | All fingers closed | S (ASL) / Closed |
| ✋ **Open Palm** | All 5 fingers extended | Hello / Stop / 5 |

## 💡 Tips for Best Results

### ✅ DO
- ✓ Use good, even lighting
- ✓ Keep hands 30-60cm from camera
- ✓ Hold gestures steady for 1 second
- ✓ Use plain background
- ✓ Face camera directly

### ❌ DON'T
- ✗ Move hands too quickly
- ✗ Use cluttered background
- ✗ Position hands too close/far
- ✗ Overlap hands unnecessarily
- ✗ Work in dim lighting

## 🎨 Visual Indicators

### Hand Colors
- **Pink/Magenta** = Right hand
- **Blue/Purple** = Left hand

### Confidence Colors
- **Green** = High confidence (>80%)
- **Orange** = Medium confidence (50-80%)
- **Red** = Low confidence (<50%)

## 📊 On-Screen Display

```
┌────────────────────────────────────────┐
│ Sign Language Interpreter              │ ← Title bar
├────────────────────────────────────────┤
│ Right Hand (0.96): 👍 Thumbs Up       │ ← Detection info
│ Left Hand (0.94): ✌️ Peace            │
├────────────────────────────────────────┤
│ Current: 👍 Thumbs Up                  │ ← Smoothed gesture
│ Confidence: 85%                        │ ← Confidence level
├────────────────────────────────────────┤
│ Translation:                           │ ← History
│ Hello → 👍 → ✌️                        │
├────────────────────────────────────────┤
│ Press 'q' to quit | 'c' to clear      │ ← Instructions
└────────────────────────────────────────┘
```

## 🔧 Customization

### Adjust Sensitivity
Edit in code:
```python
interpreter = SignLanguageInterpreter(
    min_detection_confidence=0.7,  # 0.0-1.0
    min_tracking_confidence=0.5,   # 0.0-1.0
    gesture_buffer_size=10         # frames
)
```

### Adjust Hold Time
```python
interpreter.gesture_hold_time = 1.0  # seconds
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Camera won't open** | • Check camera permissions<br>• Try camera_index=1 |
| **Low FPS** | • Close other apps<br>• Reduce resolution |
| **Gestures not detected** | • Improve lighting<br>• Hold steady longer |
| **Jittery detection** | • Increase tracking confidence<br>• Use larger buffer |
| **Wrong gestures** | • Hold more precisely<br>• Ensure clear visibility |

## 📚 More Information

- **Full Guide**: `docs/SIGN_LANGUAGE_GUIDE.md`
- **Implementation**: `docs/SIGN_IMPLEMENTATION.md`
- **Source Code**: `src/sign.py`

## 🎯 Example Conversation

```
Person A signs: 👋 Hello
[Displayed: "5 (Five) / Stop / Hello"]

Person A signs: 👍 Thumbs up
[Displayed: "👍 Thumbs Up / Good / Yes"]

Person A signs: ✌️ Peace
[Displayed: "2 (Two) / V / Peace"]

Translation: Hello → Yes → Peace
```

## 📞 Support

For issues or questions:
1. Check troubleshooting guide above
2. Review full documentation
3. Open GitHub issue

---

**Version**: 1.0
**Last Updated**: November 1, 2025
**Framework**: MediaPipe Hands

---

### Remember: 
**Hold gestures steady for 1 second** for best recognition!

🤟 Happy Signing! 🤟
