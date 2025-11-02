import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def print_main_menu():
    """Display the main application menu."""
    print("\n" + "="*80)
    print("  🌉 BRIDGING WORLDS - AI-POWERED ACCESSIBILITY PLATFORM")
    print("="*80)
    print("\nChoose an application:\n")
    print("  1. 🆕 Sign Language Interpreter (Hand Keypoint Detection + TTS)")
    print("  2. 👁️  AI Vision Assistant (Object Detection + Scene Description)")
    print("  3. ℹ️  About & Documentation")
    print("  4. 🚪 Exit")
    print("\n" + "="*80)


def check_model_exists():
    """Check if a trained model exists."""
    model_path = Path(__file__).parent / 'models' / 'asl_model_best.pth'
    return model_path.exists()


def run_sign_language_interpreter():
    """Run the advanced sign language interpreter with hand keypoint detection."""
    print("\n" + "=" * 80)
    print("  🆕 ADVANCED SIGN LANGUAGE INTERPRETER")
    print("=" * 80)
    print("\n✨ Features:")
    print("  • Real-time hand keypoint detection (21 landmarks per hand)")
    print("  • Sign language gesture interpretation")
    print("  • Text-to-Speech output")
    print("  • Interactive learning mode")
    print("  • Dual-hand tracking")
    print("\n🎮 Controls:")
    print("  SPACE  - Advance to next word and speak it")
    print("  R      - Reset to beginning")
    print("  L      - Toggle keypoint labels")
    print("  K      - Toggle enhanced visualization")
    print("  S      - Save screenshot")
    print("  Q      - Quit")
    print("\n" + "=" * 80 + "\n")
    
    try:
        # Import here to avoid issues if dependencies aren't installed
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "hand_keypoint_detection",
            os.path.join(os.path.dirname(__file__), 'src', 'hand_keypoint_detection.py')
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main()
    except KeyboardInterrupt:
        print("\nReturning to menu...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to continue...")


def run_vision_assistant():
    """Run the AI vision assistant application."""
    print("\n" + "=" * 80)
    print("  👁️  AI VISION ASSISTANT")
    print("=" * 80)
    print("\n✨ Features:")
    print("  • Real-time object detection (80+ object classes)")
    print("  • Scene description with natural language")
    print("  • Audio feedback for accessibility")
    print("  • Spatial awareness and tracking")
    print("\n🎮 Controls:")
    print("  S - Analyze and describe the scene with voice")
    print("  Q - Quit the application")
    print("\n" + "=" * 80 + "\n")
    
    try:
        from vision_assistant import VisionAssistant
        assistant = VisionAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nReturning to menu...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to continue...")


def show_documentation():
    """Show documentation and help information."""
    print("\n" + "=" * 80)
    print("  📖 BRIDGING WORLDS - DOCUMENTATION")
    print("=" * 80)
    print("\n🌟 About This Project:")
    print("  Bridging Worlds is an AI-powered accessibility platform that provides:")
    print("  • Real-time sign language interpretation")
    print("  • Vision assistance for accessibility")
    print("  • Text-to-Speech integration")
    print("  • Hand keypoint detection with 21 landmarks per hand")
    print("\n📚 Available Programs:")
    print("  1. Sign Language Interpreter")
    print("     - 21-point hand keypoint detection")
    print("     - Real-time gesture interpretation")
    print("     - Text-to-Speech output")
    print("     - Interactive learning mode")
    print("     - Mirror-corrected display")
    print("")
    print("  2. Vision Assistant")
    print("     - YOLOv8 object detection")
    print("     - Scene description")
    print("     - Audio announcements")
    print("     - Spatial awareness")
    print("\n📚 Documentation Files:")
    print("  • README.md - Main project overview and quick start")
    print("  • docs/hand_keypoint_tts_usage.md - Sign language interpreter guide")
    print("  • docs/vision_assistant_guide.md - Vision assistant documentation")
    print("  • docs/README.md - Complete documentation index")
    print("  • docs/QUICK_START.md - 5-minute setup guide")
    print("\n🔗 Quick Links:")
    print("  • GitHub: https://github.com/jongyuldev/bridging-worlds")
    print("  • Author: jongyuldev")
    print("\n💡 Getting Started:")
    print("  Recommended: Start with the Sign Language Interpreter (Option 1)")
    print("  - Shows hand keypoints in real-time")
    print("  - Includes Text-to-Speech output")
    print("  - Has interactive learning mode")
    print("\n🆘 Troubleshooting:")
    print("  • Camera not working? Close other apps using the camera")
    print("  • No sound? Check Windows TTS settings and volume")
    print("  • Poor detection? Improve lighting and clear background")
    print("  • Mirror issue? All programs now have mirror-corrected display!")
    print("\n🎯 System Requirements:")
    print("  • Python 3.8+")
    print("  • Webcam (720p or higher recommended)")
    print("  • 4GB+ RAM")
    print("  • Windows 10/11 (for TTS features)")
    print("  • Good lighting conditions")
    print("\n" + "=" * 80)
    input("\nPress Enter to return to main menu...")


def main():
    """Main application entry point."""
    while True:
        print_main_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            run_sign_language_interpreter()
        
        elif choice == '2':
            run_vision_assistant()
        
        elif choice == '3':
            show_documentation()
        
        elif choice == '4':
            print("\n" + "=" * 80)
            print("  Thank you for using Bridging Worlds! 🌉")
            print("  Empowering communication through AI - One gesture at a time ✋")
            print("=" * 80 + "\n")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice. Please enter 1-4.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        print("\n" + "=" * 80)
        print("  🌉 BRIDGING WORLDS")
        print("  AI-Powered Sign Language Interpretation & Vision Assistance")
        print("=" * 80)
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated by user. Goodbye!")
        sys.exit(0)
