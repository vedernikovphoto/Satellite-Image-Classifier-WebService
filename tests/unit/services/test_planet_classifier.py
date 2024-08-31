import numpy as np
from src.containers.containers import AppContainer


def test_predicts_not_fail(app_container: AppContainer, sample_image_np: np.ndarray):
    """
    Test that the prediction methods of the PlanetClassifier do not raise exceptions.

    This test ensures that both the `predict` and `predict_proba` methods can be called
    without errors on a sample image.
    """
    planet_classifier = app_container.planet_classifier()
    planet_classifier.predict(sample_image_np)
    planet_classifier.predict_proba(sample_image_np)


def test_prob_less_or_equal_to_one(app_container: AppContainer, sample_image_np: np.ndarray):
    """
    Test that the predicted probabilities are within the valid range [0, 1].

    This test checks that all probabilities returned by the `predict_proba` method
    are between 0 and 1, inclusive.
    """
    planet_classifier = app_container.planet_classifier()
    planet2prob = planet_classifier.predict_proba(sample_image_np)
    for planet, prob in planet2prob.items():
        if prob < 0 or prob > 1:
            raise AssertionError(f"Probability for planet '{planet}' is out of range: {prob}")
