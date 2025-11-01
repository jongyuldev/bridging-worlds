"""
Quick test script to verify TTS is working
"""
import sys

if sys.platform == 'win32':
    import win32com.client
    
    print("Testing Windows TTS...")
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Rate = 1
    speaker.Volume = 100
    
    text = "Hello! Text to speech is working correctly."
    print(f"Speaking: {text}")
    speaker.Speak(text)
    print("TTS test complete!")
else:
    print("This test is for Windows only")
