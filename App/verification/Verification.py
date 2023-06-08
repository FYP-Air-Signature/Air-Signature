from App.verification.ModelVerifier import ModelVerifier
from App.verification.Preprocess import preprocessAndResizeV1
from App.verification.air_signature_model.TensorFlowModelLoader import TensorFlowModelLoader
from App.verification.distances.L1Dist import L1Dist
from dotenv import dotenv_values
import tensorflow as tf

# Load environment variables from .env file
env_vars = dotenv_values()

class Verification:
    def __init__(self):
        self.model_loader = TensorFlowModelLoader(env_vars["CURRENT_MODEL_VERSION"])
        self.model_verifier = None

    def verify_signature(self, user, new_img_name="new_sign.png"):
        if self.model_verifier is None:

            # TODO: here you can update custom objects of model
            self.model_loader.load_model(customObjects= {'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})
            model = self.model_loader.get_model()

            # TODO: here you can update preprocess function of model
            self.model_verifier = ModelVerifier(model, env_vars["DETECTION_THRESHOLD"], env_vars["VERIFICATION_THRESHOLD"], preprocess=preprocessAndResizeV1)

        results, verified = self.model_verifier.verify(user, new_img_name)
        return results, verified

