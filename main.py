"""
Main entry point for Bridging Worlds applications.
Choose between Vision Assistant or ASL Sign Language Translator.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def print_main_menu():
    """Display the main application menu."""
    print("\n" + "="*70)
    print("  BRIDGING WORLDS - ACCESSIBILITY TOOLS")
    print("="*70)
    print("\nChoose an application:\n")
    print("  1. Vision Assistant (for the blind)")
    print("  2. ASL Sign Language Translator")
    print("  3. Exit")
    print("\n" + "="*70)


def print_asl_menu():
    """Display ASL translator menu."""
    print("\n" + "="*60)
    print("  ASL SIGN LANGUAGE TRANSLATOR")
    print("="*60)
    print("\nChoose a mode:\n")
    print("  1. Basic Recognition (MediaPipe - No training required)")
    print("  2. Advanced Recognition (CNN Model - High accuracy)")
    print("  3. Train New Model")
    print("  4. Back to Main Menu")
    print("\n" + "="*60)


def check_model_exists():
    """Check if a trained model exists."""
    model_path = Path(__file__).parent / 'models' / 'asl_model_best.pth'
    return model_path.exists()


def run_vision_assistant():
    """Run the vision assistant application."""
    print("\n" + "=" * 70)
    print("  VISION ASSISTANT FOR THE BLIND")
    print("=" * 70)
    print("\nStarting the application...")
    print("\nControls:")
    print("  Press 'S' - Analyze and describe the scene with voice")
    print("  Press 'Q' - Quit the application")
    print("\n" + "=" * 70 + "\n")
    
    try:
        from vision_assistant import VisionAssistant
        assistant = VisionAssistant()
        assistant.run()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to continue...")


def run_asl_translator():
    """Run the ASL sign language translator with submenu."""
    while True:
        print_asl_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\nStarting Basic Recognition Mode...")
            print("This mode uses MediaPipe for simple gesture detection.\n")
            try:
                from sign_language import SignLanguageTranslator
                translator = SignLanguageTranslator()
                translator.run()
            except KeyboardInterrupt:
                print("\nReturning to menu...")
            except Exception as e:
                print(f"\nError: {e}")
                input("Press Enter to continue...")
        
        elif choice == '2':
            print("\nStarting Advanced Recognition Mode...")
            
            if not check_model_exists():
                print("\nWARNING: No trained model found!")
                print("Please train a model first (option 3) or the recognition won't work.")
                response = input("\nContinue anyway? (y/n): ").strip().lower()
                if response != 'y':
                    continue
            
            try:
                from asl_translator import AdvancedSignLanguageTranslator
                translator = AdvancedSignLanguageTranslator()
                translator.run()
            except KeyboardInterrupt:
                print("\nReturning to menu...")
            except Exception as e:
                print(f"\nError: {e}")
                input("Press Enter to continue...")
        
        elif choice == '3':
            print("\nStarting Model Training...")
            print("This will take 20-30 minutes depending on your hardware.\n")
            
            response = input("Continue? (y/n): ").strip().lower()
            if response != 'y':
                continue
            
            try:
                from train_asl_model import main as train_main
                train_main()
                print("\nTraining completed successfully!")
                input("Press Enter to continue...")
            except KeyboardInterrupt:
                print("\nTraining interrupted.")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"\nError during training: {e}")
                input("Press Enter to continue...")
        
        elif choice == '4':
            break
        
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")
            input("Press Enter to continue...")


def main():
    """Main application entry point."""
    while True:
        print_main_menu()
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            run_vision_assistant()
        
        elif choice == '2':
            run_asl_translator()
        
        elif choice == '3':
            print("\nThank you for using Bridging Worlds!")
            print("Goodbye!\n")
            sys.exit(0)
        
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Goodbye!")
        sys.exit(0)
