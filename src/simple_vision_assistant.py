"""
Simplified Vision Assistant for the Blind
A lightweight version using OpenCV's pre-trained models
Requires fewer dependencies and is easier to set up.
"""

import cv2
import numpy as np
import pyttsx3
import time
import threading

class SimpleVisionAssistant:
    def __init__(self):
        """Initialize the simplified vision assistant."""
        print("Initializing Simple Vision Assistant...")
        
        # Initialize Text-to-Speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 1.0)
        
        # Load COCO class names
        self.classes = self._load_coco_names()
        
        # Load pre-trained MobileNet SSD model
        print("Loading object detection model...")
        self.net = cv2.dnn.readNetFromCaffe(
            'models/MobileNetSSD_deploy.prototxt',
            'models/MobileNetSSD_deploy.caffemodel'
        )
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open webcam")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Timing for announcements
        self.last_announcement = time.time()
        self.announcement_interval = 5
        
        self.is_speaking = False
        self.speech_queue = []
        
        print("Simple Vision Assistant initialized!")
        self.speak("Simple Vision Assistant activated.")
    
    def _load_coco_names(self):
        """Load class names for MobileNet SSD."""
        return ['background', 'aeroplane', 'bicycle', 'bird', 'boat',
                'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable',
                'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep',
                'sofa', 'train', 'tvmonitor']
    
    def speak(self, text, priority=False):
        """Text to speech with queue."""
        if priority:
            self.speech_queue = [text]
        else:
            self.speech_queue.append(text)
        
        if not self.is_speaking:
            threading.Thread(target=self._process_speech, daemon=True).start()
    
    def _process_speech(self):
        """Process speech queue."""
        self.is_speaking = True
        while self.speech_queue:
            text = self.speech_queue.pop(0)
            print(f"Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        self.is_speaking = False
    
    def detect_objects(self, frame):
        """Detect objects using MobileNet SSD."""
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        
        self.net.setInput(blob)
        detections = self.net.forward()
        
        results = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > 0.5:  # 50% confidence threshold
                class_id = int(detections[0, 0, i, 1])
                if class_id < len(self.classes):
                    class_name = self.classes[class_id]
                    
                    # Get bounding box
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    x1, y1, x2, y2 = box.astype(int)
                    
                    results.append({
                        'class': class_name,
                        'confidence': confidence,
                        'bbox': [x1, y1, x2, y2]
                    })
        
        return results
    
    def describe_scene(self, detections, frame_width):
        """Create scene description."""
        if not detections:
            return "No objects detected."
        
        # Count objects
        object_counts = {}
        for det in detections:
            class_name = det['class']
            if class_name != 'background':
                object_counts[class_name] = object_counts.get(class_name, 0) + 1
        
        if not object_counts:
            return "No objects detected."
        
        # Create description
        description = []
        for class_name, count in object_counts.items():
            if count == 1:
                description.append(f"one {class_name}")
            else:
                description.append(f"{count} {class_name}s")
        
        if len(description) == 1:
            return f"I see {description[0]}"
        elif len(description) == 2:
            return f"I see {description[0]} and {description[1]}"
        else:
            return f"I see {', '.join(description[:-1])}, and {description[-1]}"
    
    def draw_detections(self, frame, detections):
        """Draw detections on frame."""
        for det in detections:
            if det['class'] == 'background':
                continue
            
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            label = f"{det['class']} {det['confidence']:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame
    
    def run(self):
        """Main loop."""
        print("Starting Simple Vision Assistant...")
        print("Press 'q' to quit, 's' for scene description")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Detect objects
                detections = self.detect_objects(frame)
                
                # Auto-announce
                current_time = time.time()
                if current_time - self.last_announcement > self.announcement_interval:
                    description = self.describe_scene(detections, frame.shape[1])
                    self.speak(description)
                    self.last_announcement = current_time
                
                # Draw
                frame = self.draw_detections(frame, detections)
                
                cv2.putText(frame, f"Detected: {len(detections)}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Simple Vision Assistant', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.speak("Goodbye", priority=True)
                    break
                elif key == ord('s'):
                    description = self.describe_scene(detections, frame.shape[1])
                    self.speak(description, priority=True)
        
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

def main():
    try:
        assistant = SimpleVisionAssistant()
        assistant.run()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
