import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        model = load_model(os.path.join("artifacts", "training", "model.h5"))

       
        test_image = image.load_img(self.filename, target_size=(224, 244))  
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

       
        test_image = test_image / 255.0

        # Predict
        prediction_probs = model.predict(test_image)
        result = np.argmax(prediction_probs, axis=1)[0]

        # Map prediction
        if result == 1:
            prediction = "Healthy"
        else:
            prediction = "Coccidiosis"

        return [{"image": prediction}]
