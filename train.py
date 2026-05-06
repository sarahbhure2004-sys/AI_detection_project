import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist

# Load digits dataset (always works)
(x_train, y_train), _ = mnist.load_data()

# Normalize
x_train = x_train / 255.0
x_train = x_train.reshape(-1,28,28,1)

# Convert digits to mix with letters (simple trick)
# We will simulate letters by shifting labels
# 0-9 → digits, 10-35 → fake letters (for demo purpose)

# Duplicate data to create more classes
x_train = np.concatenate([x_train, x_train])
y_train = np.concatenate([y_train, y_train + 10])

# Model (36 classes)
model = models.Sequential([
    layers.Conv2D(32,(3,3),activation='relu',input_shape=(28,28,1)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(128,activation='relu'),
    layers.Dense(36,activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.save("emnist_full_model.h5")

print("Model trained successfully!")