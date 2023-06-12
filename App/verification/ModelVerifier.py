import os
import numpy as np


class ModelVerifier:

    def __init__(self, model, detection_threshold, verification_threshold, preprocess):
        self.model = model
        self.detection_threshold = float(detection_threshold)
        self.verification_threshold = float(verification_threshold)
        self.preprocess = preprocess

    def verify(self, user):
        verification_images_dir = os.path.join('verification', 'application_data', user, 'verification_images')
        verification_images = os.listdir(verification_images_dir)

        pos_groups, inp_groups = [], []

        verification_images.sort()
        images_pos = [os.path.join('verification', 'application_data', user, 'verification_images', x) for x in verification_images]
        images_inp = [os.path.join('verification', 'application_data', user, 'new_sign', 'convertedSign.png')]
        inp_groups.append(images_inp)
        pos_groups.append(images_pos)

        del images_pos, images_inp

        signs_gen = self.preprocess(pos_groups, inp_groups, user)

        prediction = []

        for i in range(5):
            (img1, img2) = next(signs_gen)
            prediction.append(self.model.predict([img1, img2])[0][0])

        detection = np.sum(np.array(prediction) <= self.detection_threshold)
        verification = detection / len(verification_images)
        verified = verification > self.verification_threshold

        return prediction, verified
