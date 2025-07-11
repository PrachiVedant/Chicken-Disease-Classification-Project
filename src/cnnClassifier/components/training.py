from pathlib import Path
import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from cnnClassifier import logger
import time
from cnnClassifier.entity.config_entity import TrainingModelConfig

tf.config.run_functions_eagerly(True)
print("Eager execution:", tf.executing_eagerly())
class Training :
    def __init__(self, config : TrainingModelConfig):
        self.config = config
        

    # load the model
    def get_base_model(self):
        self.model= tf.keras.models.load_model(self.config.updated_base_model_path)
        self.model.compile(
            optimizer=tf.keras.optimizers.SGD(),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def train_valid_generator(self):
        # create a data generator for training and validation data
        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split = 0.20
        )
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )
        # reads the image and picks only the validation data
        valid_datageneartor = tf.keras.preprocessing.image.ImageDataGenerator(** datagenerator_kwargs)

        self.valid_generator = valid_datageneartor.flow_from_directory(
            directory = self.config.training_data,
            subset= "validation",
            shuffle = False,
            **dataflow_kwargs
        )
        if self.config.params_is_augmentation :
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range = 40,
                horizontal_flip = True,
                width_shift_range = 0.2,
                height_shift_range = 0.2,
                shear_range = 0.2,
                zoom_range=0.2,
                ** datagenerator_kwargs
            )
        else:
            train_datagenerator = valid_datageneartor

        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="training",
            shuffle=True,
            **dataflow_kwargs
        )
    @staticmethod
    def save_model(path : Path , model : tf.keras.Model):
        model.save(path)

    def train(self, callbacks_list: list):
        self.steps_per_epochs = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

        #training the model
        self.model.fit(
            self.train_generator,
            epochs=self.config.params_epochs,
            validation_steps=self.validation_steps,
            validation_data = self.valid_generator,
            callbacks = callbacks_list
            
        )

        self.save_model(
            path = self.config.trained_model_path,
            model = self.model
        )






    