import tensorflow as tf
from App.verification.distances.L1Dist import L1Dist
from App.verification.air_signature_model.siamese_model import siamese_model
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values()


class TensorFlowModelLoader:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None

    def load_model(self, **customObjects):
        # self.model = tf.keras.models.load_model(self.model_path, custom_objects=customObjects)
        self.model = siamese_model((int(env_vars["IMG_H"]), int(env_vars["IMG_W"]), 1))

        self.model.load_weights(self.model_path)

    def get_model(self):
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        return self.model


if __name__ == "__main__":
    tfl = TensorFlowModelLoader("v1\\weights\\AirSig-CEDAR-009.h5")
    tfl.load_model()
    print(tfl.get_model().summary())
