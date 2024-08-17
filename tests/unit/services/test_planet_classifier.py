from copy import deepcopy

import numpy as np

from src.containers.containers import AppContainer


def test_predicts_not_fail(app_container: AppContainer, sample_image_np: np.ndarray):
    planet_classifier = app_container.planet_classifier()
    planet_classifier.predict(sample_image_np)
    planet_classifier.predict_proba(sample_image_np)


def test_prob_less_or_equal_to_one(app_container: AppContainer, sample_image_np: np.ndarray):
    planet_classifier = app_container.planet_classifier()
    planet2prob = planet_classifier.predict_proba(sample_image_np)
    for planet, prob in planet2prob.items():
        if prob < 0 or prob > 1:
            raise AssertionError(f"Probability for planet '{planet}' is out of range: {prob}")


def test_predict_dont_mutate_initial_image(app_container: AppContainer, sample_image_np: np.ndarray):
    initial_image = deepcopy(sample_image_np)
    planet_classifier = app_container.planet_classifier()
    planet_classifier.predict(sample_image_np)

    if not np.allclose(initial_image, sample_image_np):
        raise AssertionError('The input image was mutated during prediction.')
