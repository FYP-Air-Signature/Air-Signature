import os
import numpy as np


class ModelVerifier:

    def __init__(self, model, detection_threshold, verification_threshold, preprocess):
        self.model = model
        self.detection_threshold = float(detection_threshold)
        self.verification_threshold = float(verification_threshold)
        self.preprocess = preprocess

    def verify(self, user, new_img_name="new_sign.png"):
        results = []
        verification_images_dir = os.path.join('verification', 'application_data', user, 'verification_images')
        verification_images = os.listdir(verification_images_dir)
        num_verification_images = len(verification_images)

        for image in verification_images:
            input_img = self.preprocess(os.path.join('verification', 'application_data', user, 'new_sign', new_img_name))
            validation_img = self.preprocess(os.path.join(verification_images_dir, image))

            # Make Predictions
            result = self.model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
            results.append(result)

        detection = np.sum(np.array(results) <= self.detection_threshold)
        verification = detection / num_verification_images
        verified = verification > self.verification_threshold

        return results, verified
