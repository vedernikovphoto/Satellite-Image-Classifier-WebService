from copy import deepcopy
import numpy as np
from src.containers.containers import AppContainer


def test_predict_dont_mutate_initial_image(app_container: AppContainer, sample_image_np: np.ndarray):
    initial_image = deepcopy(sample_image_np)
    planet_classifier = app_container.planet_classifier()
    planet_classifier.predict(sample_image_np)

    if not np.allclose(initial_image, sample_image_np):
        raise AssertionError('The input image was mutated during prediction.')
