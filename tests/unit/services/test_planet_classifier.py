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
