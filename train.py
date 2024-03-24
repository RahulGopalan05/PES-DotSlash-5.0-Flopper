# Python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the ImageDataGenerator for data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values to [0,1]
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    validation_split=0.2  # set validation split
)

# Load the training data from the directories
train_data = datagen.flow_from_directory(
    'ASL_Dataset/train',  # directory path
    target_size=(28, 28),
    color_mode='grayscale',
    class_mode='categorical',
    batch_size=32,
    subset='training'  # set as training data
)

# Load the validation data from the directories
validation_data = datagen.flow_from_directory(
    'ASL_Dataset/test',  # same directory as training data
    target_size=(28, 28),
    color_mode='grayscale',
    class_mode='categorical',
    batch_size=32,
    subset='validation'  # set as validation data
)

# Define the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(28, activation='softmax')  # 28 classes for the 26 letters, Space, and Nothing
])

# Compile the model
model.compile(optimizer='adam', 
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])

# Fit the model on the augmented data
model.fit(train_data,
          epochs=10,
          validation_data=validation_data)

# Save the trained model
model.save('my_model.h5')
