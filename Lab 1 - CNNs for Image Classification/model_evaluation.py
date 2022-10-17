import tensorflow as tf
import tensorflow_datasets as tfds
keras = tf.keras
import keras.layers as layers
import math


def splitting_cifar_dataset_in_train_and_validation():
    (train_ds, val_ds), meta = tfds.load(
                                        'cifar10',
                                        as_supervised = True,
                                        with_info = True,
                                        split = [ 'train[:80%]', 'train[20%:]']
                                        )


def cnn_to_train_and_predict_on_cifar():
    input = tf.keras.Input(shape = (32, 32, 3))
    layer = input

    for _ in range(2):
        layer = layers.Conv2D(64, (5, 5), activation = "relu")(layer)
        layer = layers.MaxPool2D((2, 2))(layer)
    layer = layers.Flatten()(layer)
    for u, a in zip([64, 10], ["relu", "softmax"]):
        layer = layers.Dense(u, activation = a)(layer)
    model = tf.keras.Model(inputs = input, outputs = layer)

    model.compile(
        optimizer = "adam",
        loss = "sparse_categorical_crossentropy",
        metrics = ["accuracy"]
    )

    batch_size = 64
    (train_ds, val_ds), meta = tfds.load(
                                        'cifar10',
                                        as_supervised = True,
                                        with_info = True,
                                        split = [ 'train[:80%]', 'train[20%:]']
                                        )

    n_samples = meta.splits['train'].num_examples
    model.fit(
    train_ds.batch(batch_size).repeat(),
    steps_per_epoch = math.ceil(n_samples * 0.8 / batch_size),
    epochs = 5,
    validation_data = val_ds.batch(batch_size),
    validation_steps = math.ceil(n_samples * 0.2 / batch_size),
    )


def main():
    cnn_to_train_and_predict_on_cifar()

if __name__ == "__main__":
    main()