# Python
import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np

# Load the trained model
model = tf.keras.models.load_model('my_model.h5')

# Define the labels
labels = [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['Space', 'Nothing']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image from BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb)

    # Draw hand landmarks and predict gesture
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get bounding box coordinates around the hand
            x, y, w, h = cv2.boundingRect(np.int0([[lmk.x * frame.shape[1], lmk.y * frame.shape[0]] for lmk in hand_landmarks.landmark]))

            # Ensure coordinates are within frame dimensions
            height, width = frame.shape[:2]
            x = max(0, min(x, width - 1))
            y = max(0, min(y, height - 1))
            w = min(width - x, w)
            h = min(height - y, h)

            # Check if bounding box is not empty
            if w > 0 and h > 0:
                # Extract hand image
                hand_img = frame[y:y+h, x:x+w]
                hand_img = cv2.resize(hand_img, (28, 28))
                hand_img = cv2.cvtColor(hand_img, cv2.COLOR_BGR2GRAY)
                hand_img = hand_img / 255.0
                hand_img = hand_img.reshape(1, 28, 28, 1)

                # Predict gesture
                prediction = model.predict(hand_img)
                gesture = labels[np.argmax(prediction)]

                # Draw bounding box and prediction on the frame
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, str(gesture), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Hand Gesture Recognition', frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
