import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp



def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

mp_holistic=mp.solutions.holistic
mp_drawing=mp.solutions.drawing_utils

def draw_landmarks(image, results):
    # # Draw face mesh connections
    # mp_drawing.draw_landmarks(
    #     image=image,
    #     landmark_list=results.face_landmarks,
    #     connections=mp.solutions.face_mesh_connections.FACEMESH_CONTOURS,
    #     landmark_drawing_spec=None,
    #     connection_drawing_spec=mp_drawing.DrawingSpec(color=(80,110,10), thickness=1)
    # )
    
    # Draw pose connections (body sensors)
    # if results.pose_landmarks:
    #     mp_drawing.draw_landmarks(
    #         image=image,
    #         landmark_list=results.pose_landmarks,
    #         connections=mp.solutions.pose.POSE_CONNECTIONS,
    #         landmark_drawing_spec=mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
    #         connection_drawing_spec=mp_drawing.DrawingSpec(color=(80,44,121), thickness=2)
    #)
    
    # Draw left hand connections
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=results.left_hand_landmarks,
            connections=mp.solutions.hands.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(121,44,250), thickness=2)
        )
    
    # Draw right hand connections
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=results.right_hand_landmarks,
            connections=mp.solutions.hands.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(245,66,230), thickness=2)
    )


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise SystemExit("Cannot open webcam. Check camera device index and grant permission to access the camera.")

# Set mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.5,
                           min_tracking_confidence=0.5,
                           enable_segmentation= False,
                           model_complexity= 1,
                           refine_face_landmarks= False) as holistic:
    #frame = None
    while True:

        # Read feed
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        
        
        # Draw landmarks
        draw_landmarks(image, results)

        # Show to screen
        cv2.imshow('Hand Tracking', image)

        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()
if frame is not None:
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# pose = []
# for res in results.pose_landmarks.landmark:
#     test = np.array([res.x, res.y, res.z, res.visibility])
#     pose.append(test)

# pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(132)
# face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(1404)
# lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
# rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
# if results.face_landmarks:
#     # Extract x, y, z coordinates for all 468 face landmarks (468 * 3 = 1404)
#     face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten()
# else:
#     # If no face landmarks detected, return zero array of same size
#     face = np.zeros(1404)
# def extract_keypoints(results):
#     pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
#     face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
#     lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
#     rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
#     return np.concatenate([pose, face, lh, rh])
# result_test = extract_keypoints(results)
# cap = cv2.VideoCapture(0)
# cap.set(3, 1920)
# cap.set(4, 1080)

# while True:
#     ret, img= cap.read()
#     cv2.imshow('Webcam', img)

#     if cv2.waitKey(1) == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
