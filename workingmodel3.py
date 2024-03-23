# Python
import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np
import time
import pyttsx3
import keyboard

# Load the trained model
model = tf.keras.models.load_model('hand_gesture_model.h5')

# Define the labels
labels = [chr(i) for i in range(ord('A'), ord('S')+1)] + ['Space'] + [chr(i) for i in range(ord('T'), ord('Z')+1)] + ['Nothing']

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Start video capture
cap = cv2.VideoCapture(0)

# Initialize the sentence and the last prediction
sentence = ''
last_prediction = None
prediction_start_time = None

def tts(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume level

    # Convert text to speech
    engine.say(text)
    engine.runAndWait()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image from BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb)

    # Check if any hand is detected
    if results.multi_hand_landmarks:
        # Draw hand landmarks
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the hand landmarks
            landmarks = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark]).flatten()
            landmarks = landmarks.reshape(1, -1)

            # Predict gesture
            prediction = model.predict(landmarks)
            gesture = labels[np.argmax(prediction)]

            # If the gesture is the same for 5 seconds, add it to the sentence
            if gesture == last_prediction:
                if time.time() - prediction_start_time > 5:
                    if gesture == 'Space':
                        sentence += ' '  # Add a space to the sentence
                    else:
                        sentence += gesture
                    last_prediction = None  # Reset the last prediction
            else:
                last_prediction = gesture
                prediction_start_time = time.time()

            # Display the gesture and the sentence on the frame
            cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, sentence, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Hand Gesture Recognition', frame)

    # Check if 's' key is pressed
    if keyboard.is_pressed('s'):
        # Convert the sentence to speech
        tts(sentence)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
