"""
Sign Language Interpreter using Keypoint Detection
This module uses MediaPipe to detect hand keypoints and interpret sign language
to facilitate communication between signing and non-signing individuals.
"""

import cv2
import numpy as np
import mediapipe as mp
import time
from collections import deque
import math


class SignLanguageInterpreter:
    """
    A sign language interpreter that uses hand keypoint detection to recognize
    and translate sign language gestures in real-time.
    """
    
    def __init__(self, 
                 min_detection_confidence=0.7,
                 min_tracking_confidence=0.5,
                 gesture_buffer_size=10):
        """
        Initialize the sign language interpreter.
        
        Args:
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
            gesture_buffer_size: Number of frames to smooth gesture recognition
        """
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize hands detector
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=4,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Gesture recognition
        self.gesture_buffer = deque(maxlen=gesture_buffer_size)
        self.current_gesture = "None"
        self.gesture_confidence = 0.0
        
        # Translation history
        self.translation_history = deque(maxlen=5)
        self.last_gesture_time = time.time()
        self.gesture_hold_time = 1.0  # Seconds to hold before confirming
        
        # Color scheme
        self.colors = {
            'left_hand': (121, 44, 250),
            'right_hand': (245, 66, 230),
            'text_bg': (0, 0, 0),
            'text_fg': (255, 255, 255),
            'confidence_high': (0, 255, 0),
            'confidence_medium': (0, 165, 255),
            'confidence_low': (0, 0, 255)
        }
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point1.x - point2.x)**2 + 
                        (point1.y - point2.y)**2 + 
                        (point1.z - point2.z)**2)
    
    def calculate_angle(self, point1, point2, point3):
        """
        Calculate angle at point2 formed by point1-point2-point3.
        Returns angle in degrees.
        """
        # Convert to numpy arrays
        p1 = np.array([point1.x, point1.y, point1.z])
        p2 = np.array([point2.x, point2.y, point2.z])
        p3 = np.array([point3.x, point3.y, point3.z])
        
        # Calculate vectors
        v1 = p1 - p2
        v2 = p3 - p2
        
        # Calculate angle
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)  # Handle numerical errors
        angle = np.arccos(cos_angle)
        
        return np.degrees(angle)
    
    def is_finger_extended(self, hand_landmarks, finger_tip_id, finger_pip_id):
        """
        Check if a finger is extended based on keypoint positions.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            finger_tip_id: Landmark ID for fingertip
            finger_pip_id: Landmark ID for PIP joint
        """
        tip = hand_landmarks.landmark[finger_tip_id]
        pip = hand_landmarks.landmark[finger_pip_id]
        wrist = hand_landmarks.landmark[0]
        
        # Finger is extended if tip is farther from wrist than PIP
        tip_distance = self.calculate_distance(tip, wrist)
        pip_distance = self.calculate_distance(pip, wrist)
        
        return tip_distance > pip_distance
    
    def count_extended_fingers(self, hand_landmarks):
        """
        Count the number of extended fingers.
        Returns tuple: (count, [thumb, index, middle, ring, pinky])
        """
        # Finger tip and PIP joint landmark IDs
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [2, 6, 10, 14, 18]
        
        extended = []
        
        # Check thumb (different logic due to orientation)
        thumb_tip = hand_landmarks.landmark[4]
        thumb_ip = hand_landmarks.landmark[3]
        thumb_mcp = hand_landmarks.landmark[2]
        
        # Thumb is extended if tip is farther from MCP than IP joint
        thumb_extended = (
            self.calculate_distance(thumb_tip, thumb_mcp) > 
            self.calculate_distance(thumb_ip, thumb_mcp)
        )
        extended.append(thumb_extended)
        
        # Check other fingers
        for tip_id, pip_id in zip(finger_tips[1:], finger_pips[1:]):
            extended.append(self.is_finger_extended(hand_landmarks, tip_id, pip_id))
        
        return sum(extended), extended
    
    def recognize_gesture(self, hand_landmarks, handedness):
        """
        Recognize sign language gesture from hand keypoints.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            handedness: Left or Right hand
            
        Returns:
            Detected gesture name
        """
        count, fingers = self.count_extended_fingers(hand_landmarks)
        
        # Get key landmarks
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
        wrist = hand_landmarks.landmark[0]
        index_mcp = hand_landmarks.landmark[5]
        
        # Number signs (0-5)
        if count == 0:
            return "0 (Zero) / A"
        elif count == 1 and fingers[1]:  # Only index finger
            return "1 (One)"
        elif count == 2 and fingers[1] and fingers[2]:  # Index and middle
            # Check if fingers are spread (V) or together
            distance = self.calculate_distance(index_tip, middle_tip)
            if distance > 0.1:
                return "2 (Two) / V / Peace"
            else:
                return "2 (Two)"
        elif count == 3 and fingers[0] and fingers[1] and fingers[2]:
            return "3 (Three)"
        elif count == 4 and not fingers[0]:  # All except thumb
            return "4 (Four)"
        elif count == 5:
            # Check if hand is open (Hello) or showing stop
            palm_center_y = (index_mcp.y + hand_landmarks.landmark[17].y) / 2
            fingertips_avg_y = (index_tip.y + middle_tip.y + ring_tip.y + pinky_tip.y) / 4
            
            if fingertips_avg_y < palm_center_y:
                return "5 (Five) / Stop / Hello"
            else:
                return "5 (Five)"
        
        # Thumbs up/down
        if fingers[0] and count == 1:
            if thumb_tip.y < wrist.y:
                return "👍 Thumbs Up / Good / Yes"
            else:
                return "👎 Thumbs Down / Bad / No"
        
        # OK sign - thumb and index forming circle
        if fingers[0] and fingers[1]:
            thumb_index_distance = self.calculate_distance(thumb_tip, index_tip)
            if thumb_index_distance < 0.05 and count == 2:
                return "👌 OK / Perfect"
        
        # Point gesture
        if count == 1 and fingers[1]:
            if index_tip.x < wrist.x - 0.15:
                return "👈 Pointing Left"
            elif index_tip.x > wrist.x + 0.15:
                return "👉 Pointing Right"
            elif index_tip.y < wrist.y - 0.15:
                return "👆 Pointing Up"
            elif index_tip.y > wrist.y + 0.15:
                return "👇 Pointing Down"
        
        # Fist
        if count == 0:
            return "✊ Fist / S"
        
        # I Love You (ASL)
        if fingers[0] and fingers[1] and fingers[4] and not fingers[2] and not fingers[3]:
            return "🤟 I Love You (ASL)"
        
        # Rock on / Heavy metal
        if fingers[1] and fingers[4] and not fingers[2] and not fingers[3]:
            if fingers[0]:
                return "🤟 I Love You (ASL)"
            else:
                return "🤘 Rock On"
        
        # Heart gesture - bent fingers forming a heart shape
        # Check if fingers are curved (tips closer to palm than they should be for extended fingers)
        if count >= 2 and count <= 3:
            # Check if index and middle fingers are somewhat extended but curved
            index_mcp_to_tip = self.calculate_distance(hand_landmarks.landmark[5], index_tip)
            middle_mcp_to_tip = self.calculate_distance(hand_landmarks.landmark[9], middle_tip)
            
            # Check if thumbs are touching or very close (heart top)
            if fingers[0]:  # Thumb involved
                # Check curvature - fingers not fully extended
                if index_mcp_to_tip < 0.15 and middle_mcp_to_tip < 0.15:
                    # Check if hand is forming a curved shape
                    thumb_index_dist = self.calculate_distance(thumb_tip, index_tip)
                    if thumb_index_dist < 0.08:
                        return "❤️ Heart"
        
        return f"Gesture ({count} fingers)"
    
    def detect_hands(self, image):
        """
        Detect hands and extract keypoints from the image.
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            image: Processed image with detections
            results: MediaPipe detection results
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        
        # Detect hands
        results = self.hands.process(image_rgb)
        
        # Convert back to BGR for OpenCV
        image_rgb.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        return image, results
    
    def draw_landmarks(self, image, results):
        """
        Draw hand landmarks and connections on the image.
        
        Args:
            image: Input image
            results: MediaPipe detection results
        """
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, 
                                                   results.multi_handedness):
                # Determine hand color
                hand_label = handedness.classification[0].label
                color = self.colors['right_hand'] if hand_label == 'Right' else self.colors['left_hand']
                
                # Draw landmarks
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
    
    def update_gesture(self, gesture):
        """
        Update gesture buffer and determine current gesture with smoothing.
        
        Args:
            gesture: Detected gesture name
        """
        self.gesture_buffer.append(gesture)
        
        # Count occurrences of each gesture in buffer
        if len(self.gesture_buffer) > 0:
            gesture_counts = {}
            for g in self.gesture_buffer:
                gesture_counts[g] = gesture_counts.get(g, 0) + 1
            
            # Get most common gesture
            most_common = max(gesture_counts.items(), key=lambda x: x[1])
            self.current_gesture = most_common[0]
            self.gesture_confidence = most_common[1] / len(self.gesture_buffer)
            
            # Add to translation history if held long enough
            current_time = time.time()
            if (self.gesture_confidence > 0.7 and 
                current_time - self.last_gesture_time > self.gesture_hold_time):
                if (len(self.translation_history) == 0 or 
                    self.translation_history[-1] != self.current_gesture):
                    self.translation_history.append(self.current_gesture)
                    self.last_gesture_time = current_time
    
    def draw_ui(self, image, results):
        """
        Draw user interface with gesture information and translation.
        
        Args:
            image: Input image
            results: MediaPipe detection results
        """
        height, width = image.shape[:2]
        
        # Draw title
        title = "Sign Language Interpreter"
        cv2.rectangle(image, (0, 0), (width, 60), self.colors['text_bg'], -1)
        cv2.putText(image, title, (10, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.colors['text_fg'], 2)
        
        # Detect and recognize gestures
        if results.multi_hand_landmarks and results.multi_handedness:
            y_offset = 80
            
            for idx, (hand_landmarks, handedness) in enumerate(
                zip(results.multi_hand_landmarks, results.multi_handedness)):
                
                hand_label = handedness.classification[0].label
                hand_score = handedness.classification[0].score
                
                # Recognize gesture
                gesture = self.recognize_gesture(hand_landmarks, hand_label)
                self.update_gesture(gesture)
                
                # Draw hand info
                hand_text = f"{hand_label} Hand ({hand_score:.2f}): {gesture}"
                cv2.putText(image, hand_text, (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['text_fg'], 2)
                y_offset += 35
        else:
            self.update_gesture("None")
        
        # Draw current gesture (smoothed)
        confidence_color = (
            self.colors['confidence_high'] if self.gesture_confidence > 0.8 else
            self.colors['confidence_medium'] if self.gesture_confidence > 0.5 else
            self.colors['confidence_low']
        )
        
        cv2.rectangle(image, (0, height - 150), (width, height - 90), 
                     self.colors['text_bg'], -1)
        cv2.putText(image, f"Current: {self.current_gesture}", 
                   (10, height - 115), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
                   confidence_color, 2)
        cv2.putText(image, f"Confidence: {self.gesture_confidence:.0%}", 
                   (10, height - 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                   confidence_color, 1)
        
        # Draw translation history
        cv2.rectangle(image, (0, height - 85), (width, height), 
                     self.colors['text_bg'], -1)
        cv2.putText(image, "Translation:", (10, height - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['text_fg'], 1)
        
        history_text = " → ".join(list(self.translation_history)[-3:]) if self.translation_history else "..."
        cv2.putText(image, history_text, (10, height - 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
        
        # Draw instructions
        cv2.putText(image, "Press 'q' to quit | 'c' to clear history", 
                   (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                   (180, 180, 180), 1)
    
    def run(self, camera_index=0):
        """
        Run the sign language interpreter with webcam feed.
        
        Args:
            camera_index: Camera device index (default: 0)
        """
        # Open webcam
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            raise SystemExit(
                f"\n❌ Cannot open camera at index {camera_index}.\n"
                f"   Troubleshooting:\n"
                f"   • Check if camera is connected\n"
                f"   • Grant camera permissions (System Preferences → Security & Privacy → Camera)\n"
                f"   • Try a different camera index (0, 1, 2, etc.)\n"
                f"   • Close other apps using the camera\n"
            )
        
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Verify camera is working
        ret, test_frame = cap.read()
        if not ret or test_frame is None:
            cap.release()
            raise SystemExit(
                f"\n❌ Camera opened but cannot read frames.\n"
                f"   Possible causes:\n"
                f"   • Camera is being used by another application\n"
                f"   • Camera driver issues\n"
                f"   • Try restarting your computer\n"
            )
        
        print("=" * 60)
        print("Sign Language Interpreter Started")
        print("=" * 60)
        print("\nControls:")
        print("  'q' - Quit")
        print("  'c' - Clear translation history")
        print("\nSupported Gestures:")
        print("  • Numbers 0-5")
        print("  • Thumbs up/down")
        print("  • OK sign")
        print("  • Peace/Victory")
        print("  • Pointing directions")
        print("  • I Love You (ASL)")
        print("  • And more...")
        print("\nHold a gesture for 1 second to add to translation.")
        print("=" * 60)
        
        try:
            # Warm up camera
            for _ in range(5):
                cap.read()
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    print("\n❌ Failed to grab frame from camera.")
                    print("   Possible reasons:")
                    print("   • Camera is in use by another application")
                    print("   • Camera permissions not granted")
                    print("   • Camera disconnected")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect hands
                image, results = self.detect_hands(frame)
                
                # Draw landmarks
                self.draw_landmarks(image, results)
                
                # Draw UI
                self.draw_ui(image, results)
                
                # Display
                cv2.imshow('Sign Language Interpreter', image)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\nQuitting...")
                    break
                elif key == ord('c'):
                    self.translation_history.clear()
                    print("\nTranslation history cleared")
        
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            
            # Safely close hands detector
            try:
                if hasattr(self, 'hands') and self.hands is not None:
                    self.hands.close()
                    self.hands = None
            except (ValueError, AttributeError):
                pass  # Already closed or not initialized
            
            # Print final translation
            if self.translation_history:
                print("\n" + "=" * 60)
                print("Final Translation:")
                print(" → ".join(self.translation_history))
                print("=" * 60)
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            if hasattr(self, 'hands') and self.hands is not None:
                self.hands.close()
                self.hands = None
        except (ValueError, AttributeError):
            # Already closed or not initialized - safe to ignore
            pass


def main():
    """Main entry point for the sign language interpreter."""
    # Create interpreter instance
    interpreter = SignLanguageInterpreter(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
        gesture_buffer_size=10
    )
    
    # Run the interpreter
    try:
        interpreter.run(camera_index=0)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
