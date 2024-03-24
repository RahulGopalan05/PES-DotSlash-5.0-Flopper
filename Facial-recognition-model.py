import cv2
import numpy as np
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('emotion_model.h5')

# Define the class labels
CLASS_LABELS  = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sadness', "Surprise"]

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Preprocess the image
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (48, 48))
    img = img.astype('float32') / 255
    img = np.expand_dims(img, axis=0)
    img = np.reshape(img, (1, 48, 48, 3))  # Reshape to include batch size dimension

    # Make a prediction
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions[0])

    # Map the predicted class index to its corresponding emotion
    predicted_emotion = CLASS_LABELS[predicted_class]

    # Display the resulting frame with predicted emotion
    cv2.putText(frame, predicted_emotion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Video', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
