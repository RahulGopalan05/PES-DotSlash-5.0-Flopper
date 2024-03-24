# Python
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the coordinates and labels
coords = np.load('coords.npy')
labels = np.load('labels.npy')

# Flatten the coordinates
coords = coords.reshape(coords.shape[0], -1)

# Encode the labels
encoder = LabelEncoder()
labels = encoder.fit_transform(labels)
labels = to_categorical(labels)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(coords, labels, test_size=0.2, random_state=42)

# Define the model
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(labels.shape[1], activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Save the model
model.save('hand_gesture_model.h5')
