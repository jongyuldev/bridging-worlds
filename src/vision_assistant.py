"""
Vision Assistant for the Blind
A computer vision application that helps blind people understand their surroundings
using object detection, scene description, and text-to-speech feedback.
"""

import cv2
import numpy as np
from datetime import datetime
import time
from collections import deque
from ultralytics import YOLO
import torch
import sys
import os

# Import TTS based on platform
if sys.platform == 'win32':
    import win32com.client

class VisionAssistant:
    def __init__(self):
        """Initialize the Vision Assistant with all necessary components."""
        print("Initializing Vision Assistant...")
        
        # Initialize Text-to-Speech engine for Windows
        if sys.platform == 'win32':
            self.tts_engine = win32com.client.Dispatch("SAPI.SpVoice")
            self.tts_engine.Rate = 1  # Speed (-10 to 10)
            self.tts_engine.Volume = 100  # Volume (0 to 100)
        
        # Initialize YOLO model for object detection
        print("Loading YOLO model...")
        # Get the model path relative to the project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        model_path = os.path.join(project_root, 'models', 'yolov8n.pt')
        
        # If model doesn't exist in models folder, download it there
        if not os.path.exists(model_path):
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            self.model = YOLO('yolov8n.pt')  # Download
            # Move to models folder
            if os.path.exists('yolov8n.pt'):
                import shutil
                shutil.move('yolov8n.pt', model_path)
        else:
            self.model = YOLO(model_path)
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open webcam")
        
        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Detection tracking
        self.detected_objects = deque(maxlen=30)  # Store last 30 frames
        
        # Distance estimation parameters
        self.known_distances = {
            'person': 1.5,  # Average distance in meters
            'car': 3.0,
            'bicycle': 2.0,
            'dog': 1.0,
            'cat': 1.0
        }
        
        print("Vision Assistant initialized successfully!")
        self.speak("Vision Assistant activated. Press S to describe the scene. Press Q to quit.")
    
    def speak(self, text):
        """Convert text to speech - synchronous and blocking."""
        print(f"Speaking: {text}")
        try:
            if sys.platform == 'win32':
                self.tts_engine.Speak(text)
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def estimate_distance(self, bbox, class_name):
        """Estimate distance based on bounding box size."""
        # Calculate bbox height
        height = bbox[3] - bbox[1]
        
        # Simple distance estimation (inverse relationship)
        # Larger objects are closer
        if height > 300:
            return "very close"
        elif height > 200:
            return "close"
        elif height > 100:
            return "at medium distance"
        else:
            return "far away"
    
    def get_position(self, bbox, frame_width):
        """Determine if object is on left, center, or right."""
        center_x = (bbox[0] + bbox[2]) / 2
        
        if center_x < frame_width * 0.33:
            return "on your left"
        elif center_x > frame_width * 0.67:
            return "on your right"
        else:
            return "in front of you"
    def get_dominant_color(self, frame, bbox):
        """Extract dominant color from the bounding box region."""
        try:
            x1, y1, x2, y2 = [int(coord) for coord in bbox]
            
            # Ensure coordinates are within frame bounds
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
            
            if x2 <= x1 or y2 <= y1:
                return None
            
            # Extract the region
            roi = frame[y1:y2, x1:x2]
            
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            # Calculate average color
            avg_color = np.mean(hsv, axis=(0, 1))
            h, s, v = avg_color
            
            # If saturation is too low, it's grayscale
            if s < 30:
                if v < 50:
                    return "black"
                elif v > 200:
                    return "white"
                else:
                    return "gray"
            
            # Map hue to color names
            if h < 10 or h > 170:
                return "red"
            elif h < 25:
                return "orange"
            elif h < 40:
                return "yellow"
            elif h < 80:
                return "green"
            elif h < 130:
                return "blue"
            elif h < 160:
                return "purple"
            else:
                return "pink"
        except:
            return None
    
    def detect_objects(self, frame):
        """Detect objects in the frame using YOLO."""
        results = self.model(frame, conf=0.5, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf[0].cpu().numpy()
                class_id = int(box.cls[0].cpu().numpy())
                class_name = self.model.names[class_id]
                
                # Get dominant color
                color = self.get_dominant_color(frame, [x1, y1, x2, y2])
                
                detections.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': confidence,
                    'class': class_name,
                    'color': color
                })
        
        return detections
    
    def analyze_scene(self, detections, frame_width):
        """Analyze the scene and create a natural language description."""
        if not detections:
            return "No objects detected in view."
        
        # Group objects by class with their details
        object_groups = {}
        
        for det in detections:
            class_name = det['class']
            position = self.get_position(det['bbox'], frame_width)
            distance = self.estimate_distance(det['bbox'], class_name)
            color = det.get('color')
            
            if class_name not in object_groups:
                object_groups[class_name] = []
            
            object_groups[class_name].append({
                'position': position,
                'distance': distance,
                'color': color
            })
        
        # Build natural language description
        description_parts = []
        
        # Convert counts to words for numbers 1-10
        number_words = {
            1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"
        }
        
        # Create description for each object type
        object_descriptions = []
        
        for class_name, items in object_groups.items():
            count = len(items)
            count_word = number_words.get(count, str(count))
            
            # Make plural if needed
            if count > 1:
                # Handle irregular plurals
                if class_name.endswith('s') or class_name.endswith('sh') or class_name.endswith('ch'):
                    plural_name = f"{class_name}es"
                elif class_name.endswith('y') and class_name not in ['toy', 'key', 'boy']:
                    plural_name = f"{class_name[:-1]}ies"
                else:
                    plural_name = f"{class_name}s"
            else:
                plural_name = class_name
            
            # Build the object phrase with color if available
            if count == 1:
                item = items[0]
                color_desc = f"{item['color']} " if item['color'] else ""
                object_desc = f"one {color_desc}{class_name}"
            else:
                # Count colors for multiple items
                colors = [item['color'] for item in items if item['color']]
                if colors and len(set(colors)) == 1:
                    # All same color
                    object_desc = f"{count_word} {colors[0]} {plural_name}"
                elif len(set(colors)) > 1 and len(colors) >= count * 0.7:
                    # Multiple colors
                    color_counts = {}
                    for c in colors:
                        color_counts[c] = color_counts.get(c, 0) + 1
                    dominant_color = max(color_counts, key=color_counts.get)
                    object_desc = f"{count_word} {plural_name}, mostly {dominant_color}"
                else:
                    object_desc = f"{count_word} {plural_name}"
            
            # Add position and distance for the first/closest item
            closest_item = min(items, key=lambda x: 0 if x['distance'] == "very close" else 1 if x['distance'] == "close" else 2 if x['distance'] == "at medium distance" else 3)
            
            if count == 1:
                full_desc = f"{object_desc} {closest_item['distance']} {closest_item['position']}"
            else:
                full_desc = f"{object_desc}, with one {closest_item['distance']} {closest_item['position']}"
            
            object_descriptions.append(full_desc)
        
        # Combine all descriptions
        if len(object_descriptions) == 1:
            return f"I see {object_descriptions[0]}."
        elif len(object_descriptions) == 2:
            return f"I see {object_descriptions[0]}, and {object_descriptions[1]}."
        else:
            # List all but last with commas, then "and" for the last one
            all_but_last = ", ".join(object_descriptions[:-1])
            return f"I see {all_but_last}, and {object_descriptions[-1]}."
    
    def draw_detections(self, frame, detections):
        """Draw bounding boxes and labels on the frame."""
        for det in detections:
            x1, y1, x2, y2 = [int(coord) for coord in det['bbox']]
            class_name = det['class']
            confidence = det['confidence']
            color = det.get('color')
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label with color if available
            if color:
                label = f"{class_name} ({color}) {confidence:.2f}"
            else:
                label = f"{class_name} {confidence:.2f}"
            
            # Add background to label for better visibility
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), (0, 255, 0), -1)
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return frame
    
    def run(self):
        """Main loop for the vision assistant."""
        print("\n" + "="*60)
        print("VISION ASSISTANT - Ready!")
        print("="*60)
        print("Controls:")
        print("  Press 'S' - Describe the scene")
        print("  Press 'Q' - Quit")
        print("="*60 + "\n")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Always detect objects for visual display
                detections = self.detect_objects(frame)
                
                # Draw detections on frame
                frame = self.draw_detections(frame, detections)
                
                # Add text overlay
                cv2.putText(frame, f"Objects detected: {len(detections)}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Press 'S' to describe scene | 'Q' to quit", 
                           (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (255, 255, 255), 1)
                
                # Display frame
                cv2.imshow('Vision Assistant', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    print("\nShutting down...")
                    self.speak("Goodbye")
                    break
                    
                elif key == ord('s') or key == ord('S'):
                    print("\n--- Analyzing scene ---")
                    # Get fresh detection for speech
                    ret, fresh_frame = self.cap.read()
                    if ret:
                        detections = self.detect_objects(fresh_frame)
                        if detections:
                            description = self.analyze_scene(detections, fresh_frame.shape[1])
                            self.speak(description)
                        else:
                            self.speak("No objects detected in view")
                    print("--- Analysis complete ---\n")
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        self.cap.release()
        cv2.destroyAllWindows()
        print("Vision Assistant shut down successfully.")

def main():
    """Main entry point."""
    try:
        assistant = VisionAssistant()
        assistant.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
