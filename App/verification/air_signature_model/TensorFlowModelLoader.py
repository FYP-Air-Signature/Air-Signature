import tensorflow as tf
from App.verification.distances.L1Dist import L1Dist


class TensorFlowModelLoader:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None

    def load_model(self, customObjects):
        self.model = tf.keras.models.load_model(self.model_path, custom_objects = customObjects)

    def get_model(self):
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        return self.model


if __name__ == "__main__":
    tfl = TensorFlowModelLoader("v1\\siamesemodelv2.h5")
    tfl.load_model({'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})
    print(tfl.get_model())
