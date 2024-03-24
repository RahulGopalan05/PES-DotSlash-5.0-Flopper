# Python
import cv2
import mediapipe as mp
import os
import numpy as np

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Define the paths to your train and test directories
train_dir = 'ASL_Dataset/Train'

# Define the labels
labels_list = [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['Space', 'Nothing']

# Initialize lists to store the coordinates and labels
coords = []
labels = []

# Process each image in the dataset
for label in labels_list:
    for filename in os.listdir(os.path.join(train_dir, label)):
        # Load the image
        img = cv2.imread(os.path.join(train_dir, label, filename))

        # Convert the image from BGR to RGB
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe Hands
        results = hands.process(rgb)

        # Check if any hand is detected
        if results.multi_hand_landmarks:
            # Get the coordinates of the hand landmarks
            landmarks = [[landmark.x, landmark.y, landmark.z] for landmark in results.multi_hand_landmarks[0].landmark]
            coords.append(landmarks)
            labels.append(label)

# Convert the lists to numpy arrays
coords = np.array(coords)
labels = np.array(labels)

# Save the coordinates and labels
np.save('coords.npy', coords)
np.save('labels.npy', labels)
