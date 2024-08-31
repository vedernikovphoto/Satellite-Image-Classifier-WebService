from copy import deepcopy
import numpy as np
from src.containers.containers import AppContainer


def test_predict_dont_mutate_initial_image(app_container: AppContainer, sample_image_np: np.ndarray):
    """
    Test that the `predict` method does not mutate the input image.

    This test ensures that the `planet_classifier.predict` method does not modify
    the original image array passed to it.
    """
    initial_image = deepcopy(sample_image_np)
    planet_classifier = app_container.planet_classifier()
    planet_classifier.predict(sample_image_np)

    if not np.allclose(initial_image, sample_image_np):
        raise AssertionError('The input image was mutated during prediction.')
