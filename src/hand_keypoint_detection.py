"""
Hand Keypoint Detection using OpenCV and MediaPipe
This program detects and tracks hand landmarks in real-time using webcam feed.
"""

import cv2
import mediapipe as mp
import numpy as np
import sys
from typing import Optional, Tuple

# Import TTS for Windows
if sys.platform == 'win32':
    import win32com.client


class HandKeypointDetector:
    """
    Detects hand keypoints using MediaPipe Hands solution.
    Each hand has 21 landmarks/keypoints.
    """
    
    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        """
        Initialize the hand keypoint detector.
        
        Args:
            static_image_mode: If False, treats input as video stream
            max_num_hands: Maximum number of hands to detect (1 or 2)
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Hand landmark names (21 points per hand)
        self.landmark_names = [
            'WRIST',
            'THUMB_CMC', 'THUMB_MCP', 'THUMB_IP', 'THUMB_TIP',
            'INDEX_FINGER_MCP', 'INDEX_FINGER_PIP', 'INDEX_FINGER_DIP', 'INDEX_FINGER_TIP',
            'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP', 'MIDDLE_FINGER_DIP', 'MIDDLE_FINGER_TIP',
            'RING_FINGER_MCP', 'RING_FINGER_PIP', 'RING_FINGER_DIP', 'RING_FINGER_TIP',
            'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP'
        ]
    
    def detect_hands(self, image: np.ndarray) -> Tuple[np.ndarray, Optional[object]]:
        """
        Detect hands and their keypoints in an image.
        
        Args:
            image: Input image in BGR format (OpenCV format)
            
        Returns:
            Tuple of (annotated_image, results)
        """
        # Convert BGR to RGB for MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = self.hands.process(image_rgb)
        
        # Draw hand landmarks
        annotated_image = image.copy()
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks and connections
                self.mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        return annotated_image, results
    
    def get_keypoint_coordinates(
        self,
        results: object,
        image_shape: Tuple[int, int, int]
    ) -> list:
        """
        Extract keypoint coordinates from detection results.
        
        Args:
            results: MediaPipe results object
            image_shape: Shape of the image (height, width, channels)
            
        Returns:
            List of dictionaries containing hand information and keypoints
        """
        if not results.multi_hand_landmarks:
            return []
        
        h, w, _ = image_shape
        hands_data = []
        
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get hand label (Left or Right)
            handedness = results.multi_handedness[idx].classification[0]
            hand_label = handedness.label
            hand_confidence = handedness.score
            
            # Extract keypoints
            keypoints = []
            for landmark_idx, landmark in enumerate(hand_landmarks.landmark):
                keypoint = {
                    'name': self.landmark_names[landmark_idx],
                    'x': int(landmark.x * w),
                    'y': int(landmark.y * h),
                    'z': landmark.z,  # Depth relative to wrist
                    'visibility': landmark.visibility if hasattr(landmark, 'visibility') else 1.0
                }
                keypoints.append(keypoint)
            
            hands_data.append({
                'hand': hand_label,
                'confidence': hand_confidence,
                'keypoints': keypoints
            })
        
        return hands_data
    
    def draw_enhanced_keypoints(
        self,
        image: np.ndarray,
        hands_data: list,
        show_labels: bool = True
    ) -> np.ndarray:
        """
        Draw keypoints with enhanced visualization including labels.
        
        Args:
            image: Input image
            hands_data: List of hand data from get_keypoint_coordinates
            show_labels: Whether to show keypoint labels
            
        Returns:
            Image with enhanced keypoint visualization
        """
        output = image.copy()
        
        for hand_data in hands_data:
            hand_label = hand_data['hand']
            keypoints = hand_data['keypoints']
            
            # Choose color based on hand
            color = (0, 255, 0) if hand_label == 'Right' else (255, 0, 0)
            
            # Draw keypoints
            for kp in keypoints:
                x, y = kp['x'], kp['y']
                
                # Draw circle for each keypoint
                cv2.circle(output, (x, y), 5, color, -1)
                cv2.circle(output, (x, y), 7, (255, 255, 255), 2)
                
                # Draw label
                if show_labels and kp['name'] in ['WRIST', 'THUMB_TIP', 'INDEX_FINGER_TIP']:
                    cv2.putText(
                        output,
                        kp['name'],
                        (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.3,
                        color,
                        1
                    )
            
            # Draw hand label
            if keypoints:
                wrist = keypoints[0]
                label_text = f"{hand_label} Hand ({hand_data['confidence']:.2f})"
                cv2.putText(
                    output,
                    label_text,
                    (wrist['x'] - 50, wrist['y'] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )
        
        return output
    
    def close(self):
        """Clean up resources."""
        self.hands.close()


class TextToSpeech:
    """
    Text-to-Speech handler for Windows.
    """
    
    def __init__(self):
        """Initialize TTS engine."""
        self.speaker = None
        if sys.platform == 'win32':
            try:
                self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
                self.speaker.Rate = 1
                self.speaker.Volume = 100
                print("TTS initialized successfully")
            except Exception as e:
                print(f"Warning: Could not initialize TTS: {e}")
        else:
            print("TTS is only available on Windows")
    
    def speak(self, text: str):
        """
        Speak the given text.
        
        Args:
            text: Text to speak
        """
        if self.speaker:
            try:
                self.speaker.Speak(text)
            except Exception as e:
                print(f"Error speaking text: {e}")
        else:
            print(f"TTS not available. Would speak: {text}")


class SentenceManager:
    """
    Manages sentence display and word progression.
    """
    
    def __init__(self, sentence: str, tts: TextToSpeech):
        """
        Initialize sentence manager.
        
        Args:
            sentence: The sentence to display word by word
            tts: TextToSpeech instance
        """
        self.words = sentence.split()
        self.current_word_index = 0
        self.tts = tts
        self.sentence = sentence
    
    def get_current_word(self) -> str:
        """Get the current word."""
        if self.current_word_index < len(self.words):
            return self.words[self.current_word_index]
        return ""
    
    def get_display_text(self) -> str:
        """Get the full sentence with current word highlighted."""
        if self.current_word_index >= len(self.words):
            return self.sentence
        
        display_words = []
        for i, word in enumerate(self.words):
            if i == self.current_word_index:
                display_words.append(f"[{word}]")
            else:
                display_words.append(word)
        
        return " ".join(display_words)
    
    def next_word(self):
        """Move to next word and speak it."""
        if self.current_word_index < len(self.words):
            current_word = self.words[self.current_word_index]
            print(f"Speaking word {self.current_word_index + 1}/{len(self.words)}: {current_word}")
            self.tts.speak(current_word)
            self.current_word_index += 1
    
    def reset(self):
        """Reset to the beginning."""
        self.current_word_index = 0
        print("Reset to beginning of sentence")
    
    def is_complete(self) -> bool:
        """Check if all words have been spoken."""
        return self.current_word_index >= len(self.words)


def main():
    """Main function to run hand keypoint detection from webcam."""
    print("Hand Keypoint Detection Program with TTS")
    print("==========================================")
    print("Controls:")
    print("  - Press 'q' to quit")
    print("  - Press 's' to save current frame")
    print("  - Press 'l' to toggle labels")
    print("  - Press 'k' to toggle enhanced keypoints")
    print("  - Press SPACE to advance to next word and speak it")
    print("  - Press 'r' to reset to beginning of sentence")
    print()
    
    # Initialize TTS
    tts = TextToSpeech()
    
    # Initialize sentence manager
    sentence = "Hello my name is John and I am a student in Durham University"
    sentence_tts = "Hello my name is J O H N and I am a student in D U R H A M University"
    sentence_manager = SentenceManager(sentence_tts, tts)
    
    print(f"Sentence: {sentence}")
    print(f"Total words: {len(sentence_manager.words)}")
    print()
    
    # Initialize detector
    detector = HandKeypointDetector(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    show_labels = True
    show_enhanced = False
    frame_count = 0
    saved_count = 0
    
    print("Starting camera... Press 'q' to quit")
    
    while True:
        success, frame = cap.read()
        
        if not success:
            print("Error: Could not read frame")
            break
        
        # Flip frame horizontally to mirror the camera (more natural for user)
        frame = cv2.flip(frame, 1)
        
        frame_count += 1
        
        # Detect hands
        annotated_frame, results = detector.detect_hands(frame)
        
        # Get keypoint data
        hands_data = detector.get_keypoint_coordinates(results, frame.shape)
        
        # Use enhanced visualization if enabled
        if show_enhanced and hands_data:
            annotated_frame = detector.draw_enhanced_keypoints(
                frame,
                hands_data,
                show_labels=show_labels
            )
        
        # Display information on frame
        info_text = f"Hands detected: {len(hands_data)}"
        cv2.putText(
            annotated_frame,
            info_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        # Display keypoint count for each hand
        y_offset = 70
        for hand_data in hands_data:
            hand_info = f"{hand_data['hand']}: {len(hand_data['keypoints'])} keypoints"
            cv2.putText(
                annotated_frame,
                hand_info,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )
            y_offset += 30
        
        # Display sentence with current word highlighted
        sentence_display = sentence_manager.get_display_text()
        
        # Add background rectangle for better text visibility
        text_bg_height = 120
        cv2.rectangle(
            annotated_frame,
            (0, annotated_frame.shape[0] - text_bg_height),
            (annotated_frame.shape[1], annotated_frame.shape[0]),
            (0, 0, 0),
            -1
        )
        cv2.rectangle(
            annotated_frame,
            (0, annotated_frame.shape[0] - text_bg_height),
            (annotated_frame.shape[1], annotated_frame.shape[0]),
            (255, 255, 255),
            2
        )
        
        # Display sentence (split into multiple lines if needed)
        max_chars_per_line = 50
        words_in_display = sentence_display.split()
        lines = []
        current_line = []
        
        for word in words_in_display:
            test_line = " ".join(current_line + [word])
            if len(test_line) <= max_chars_per_line:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(" ".join(current_line))
        
        # Display lines
        line_y = annotated_frame.shape[0] - 80
        for line in lines:
            cv2.putText(
                annotated_frame,
                line,
                (10, line_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
            line_y += 30
        
        # Display progress
        progress_text = f"Word: {sentence_manager.current_word_index}/{len(sentence_manager.words)}"
        cv2.putText(
            annotated_frame,
            progress_text,
            (10, annotated_frame.shape[0] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )
        
        # Display completion status
        if sentence_manager.is_complete():
            completion_text = "COMPLETE - Press 'r' to reset"
            cv2.putText(
                annotated_frame,
                completion_text,
                (annotated_frame.shape[1] - 400, annotated_frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        # Show frame
        cv2.imshow('Hand Keypoint Detection', annotated_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("Quitting...")
            break
        elif key == ord('s'):
            filename = f"hand_keypoints_{saved_count:03d}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"Saved: {filename}")
            saved_count += 1
        elif key == ord('l'):
            show_labels = not show_labels
            print(f"Labels: {'ON' if show_labels else 'OFF'}")
        elif key == ord('k'):
            show_enhanced = not show_enhanced
            print(f"Enhanced keypoints: {'ON' if show_enhanced else 'OFF'}")
        elif key == ord(' '):  # Space bar
            if not sentence_manager.is_complete():
                sentence_manager.next_word()
            else:
                print("Sentence complete! Press 'r' to reset.")
        elif key == ord('r'):
            sentence_manager.reset()
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
    
    print(f"\nProcessed {frame_count} frames")
    print(f"Saved {saved_count} images")
    print("Program ended successfully")


if __name__ == "__main__":
    main()
