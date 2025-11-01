import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set maximum resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Configure hand detection
# max_num_hands: Maximum number of hands to detect
# min_detection_confidence: Minimum confidence for hand detection
# min_tracking_confidence: Minimum confidence for hand tracking
with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    # Variables for FPS calculation
    prev_time = 0
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        # Flip the image horizontally for a selfie-view display
        image = cv2.flip(image, 1)
        
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to pass by reference
        image_rgb.flags.writeable = False
        
        # Process the image and detect hands
        results = hands.process(image_rgb)
        
        # Convert back to BGR for OpenCV
        image_rgb.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Draw landmarks and connections
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                # Get handedness (Left or Right)
                handedness = results.multi_handedness[hand_idx].classification[0].label
                
                # Display keypoint coordinates for specific landmarks
                # Landmark 0: Wrist
                # Landmark 4: Thumb tip
                # Landmark 8: Index finger tip
                # Landmark 12: Middle finger tip
                # Landmark 16: Ring finger tip
                # Landmark 20: Pinky tip
                
                h, w, c = image.shape
                wrist = hand_landmarks.landmark[0]
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                
                # Convert normalized coordinates to pixel coordinates
                wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                
                # Display hand information
                cv2.putText(image, f'{handedness} Hand', (wrist_x - 50, wrist_y - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Display landmark count
                cv2.putText(image, f'Landmarks: {len(hand_landmarks.landmark)}',
                           (10, 30 + hand_idx * 30), cv2.FONT_HERSHEY_SIMPLEX,
                           0.7, (255, 255, 0), 2)
        
        # Calculate and display FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(image, f'FPS: {int(fps)}', (10, image.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Display instructions
        cv2.putText(image, 'Press Q to quit', (10, image.shape[0] - 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Show the image
        cv2.imshow('Hand Keypoint Detection - MediaPipe', image)
        
        # Break loop on 'q' press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
