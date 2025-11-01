"""
Quick Demo Script for Sign Language Interpreter
Run this to test the sign language interpreter with your webcam
"""

from src.sign import SignLanguageInterpreter

def main():
    print("\n" + "="*70)
    print(" " * 15 + "🤟 SIGN LANGUAGE INTERPRETER DEMO 🤟")
    print("="*70)
    print("\n📹 Starting webcam... Please allow camera access if prompted.")
    print("\n🎯 Try these gestures:")
    print("   • Hold up 1-5 fingers for numbers")
    print("   • Thumbs up for 'Yes/Good'")
    print("   • Thumbs down for 'No/Bad'")
    print("   • Make an 'OK' sign with thumb and index finger")
    print("   • Show a peace sign (index + middle fingers)")
    print("   • Point in different directions")
    print("\n💡 Tips:")
    print("   • Keep hands clearly visible")
    print("   • Hold gestures steady for 1 second")
    print("   • Use good lighting")
    print("\n⌨️  Controls:")
    print("   • Press 'q' to quit")
    print("   • Press 'c' to clear translation history")
    print("\n" + "="*70 + "\n")
    
    # Create and run interpreter
    interpreter = SignLanguageInterpreter(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
        gesture_buffer_size=10
    )
    
    try:
        interpreter.run(camera_index=0)
    except KeyboardInterrupt:
        print("\n\n👋 Interpreter stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  • Ensure webcam is connected and not in use")
        print("  • Check camera permissions in System Preferences")
        print("  • Try a different camera index (change camera_index=0 to 1)")
    finally:
        print("\n" + "="*70)
        print("Thank you for using the Sign Language Interpreter!")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()
