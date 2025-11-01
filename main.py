"""
Main entry point for the Vision Assistant application.
Run this file to start the vision assistant for the blind.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vision_assistant import VisionAssistant

if __name__ == "__main__":
    print("=" * 70)
    print("VISION ASSISTANT FOR THE BLIND")
    print("=" * 70)
    print("\nStarting the application...")
    print("\nControls:")
    print("  Press 'S' - Analyze and describe the scene with voice")
    print("  Press 'Q' - Quit the application")
    print("\n" + "=" * 70 + "\n")
    
    try:
        assistant = VisionAssistant()
        assistant.run()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
