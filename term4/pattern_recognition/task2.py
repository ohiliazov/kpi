import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as plt

# ensure image format is channels_last
keras.backend.set_image_data_format("channels_last")

# Load and normalize CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
x_train = x_train / 255.0
x_test = x_test / 255.0

# Draw first 100 images
# rows, columns = 5, 20
# images_to_show = rows * columns

# fig = plt.gcf()
# plt.style.use('classic')
# fig.set_size_inches(columns, rows)
#
# for i, image in enumerate(x_train[:images_to_show], start=1):
#     sp = plt.subplot(rows, columns, i)
#     sp.axis('Off')
#     plt.imshow(image)
#
# plt.show()

NUM_CLASSES = 10
LEARNING_RATE = 10e-4
BATCH_SIZE = 32
EPOCHS = 16

basic_CNN = tf.keras.models.Sequential([
  keras.layers.Conv2D(32, (3, 3), padding='same', activation="relu", input_shape=x_train.shape[1:]),
  keras.layers.Conv2D(32, (3, 3), activation="relu"),
  keras.layers.MaxPooling2D(2, 2),
  keras.layers.Dropout(0.2),
  keras.layers.Conv2D(64, (3, 3), padding='same', activation="relu", input_shape=x_train.shape[1:]),
  keras.layers.Conv2D(64, (3, 3), activation="relu"),
  keras.layers.MaxPooling2D(2, 2),
  keras.layers.Dropout(0.2),
  keras.layers.Flatten(),
  keras.layers.Dense(256, activation="relu"),
  keras.layers.Dense(NUM_CLASSES, activation="softmax"),
])

basic_CNN.compile(
    optimizer=keras.optimizers.RMSprop(learning_rate=LEARNING_RATE),
    loss="sparse_categorical_crossentropy",
    metrics=["sparse_categorical_accuracy"],
)

basic_CNN_history = basic_CNN.fit(
    x_train,
    y_train,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(x_test, y_test)
)

basic_CNN.save("basicCNN")
