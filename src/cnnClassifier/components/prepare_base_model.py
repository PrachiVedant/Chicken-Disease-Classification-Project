import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from cnnClassifier import logger
from cnnClassifier.entity.config_entity import PrepareBaseModelConfig

from pathlib import Path
import tensorflow as tf
from cnnClassifier.entity.config_entity import PrepareBaseModelConfig  # if used

class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

        # 🔧 Ensure base_model_path and updated_base_model_path are Path objects
        self.base_model_path = Path(self.config.base_model_path)
        self.updated_base_model_path = Path(self.config.updated_base_model_path)

    def get_base_model(self):
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top
        )

        # 🔧 Ensure with_suffix works by using Path object
        keras_path = self.config.base_model_path.with_suffix(".keras")
        self.save_model(path=keras_path, model=self.model)

    @staticmethod
    def prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        if freeze_all:
            for layer in model.layers:
                layer.trainable = False  # 🔧 Fix: set layer.trainable not model.trainable
        elif freeze_till is not None and freeze_till > 0:
            for layer in model.layers[:-freeze_till]:
                layer.trainable = False

        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(classes, activation='softmax')(flatten_in)

        full_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
        )

        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),  # 🔧 safer to use the class version
            metrics=['accuracy']
        )

        full_model.summary()
        return full_model

    def update_model(self):
        self.model = self.prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate
        )
        self.save_model(path=self.config.updated_base_model_path, model=self.model)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
