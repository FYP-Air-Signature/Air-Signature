from App.verification.ModelVerifier import ModelVerifier
from App.verification.Preprocess import preprocess
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

    def verify_signature(self, user, new_img_name="tempSign.png"):
        if self.model_verifier is None:
            # TODO: here you can update custom objects of model
            self.model_loader.load_model()
            model = self.model_loader.get_model()

            # TODO: here you can update preprocess function of model
            self.model_verifier = ModelVerifier(model, env_vars["DETECTION_THRESHOLD"],
                                                env_vars["VERIFICATION_THRESHOLD"], preprocess=preprocess)

        results, verified = self.model_verifier.verify(user, new_img_name)
        return results, verified
