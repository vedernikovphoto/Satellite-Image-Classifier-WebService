import numpy as np
from src.containers.containers import AppContainer


class FakePlanetClassifier:
    """
    A fake classifier for testing purposes that returns fixed outputs.
    """

    def predict(self, image):
        return []

    def predict_proba(self, image):
        return {'value': 0.2}


def test_predicts_not_fail(app_container: AppContainer, sample_image_np: np.ndarray):
    """
    Test that the predict and predict_proba methods do not raise exceptions when called.

    This test uses a FakePlanetClassifier to override the actual classifier and ensures
    that the PlanetAnalytics methods run without errors.
    """
    with app_container.reset_singletons():
        with app_container.planet_classifier.override(FakePlanetClassifier()):
            planet_classifier = app_container.planet_classifier()
            planet_classifier.predict(sample_image_np)
            planet_classifier.predict_proba(sample_image_np)


def test_prob_less_or_equal_to_one(app_container: AppContainer, sample_image_np: np.ndarray):
    """
    Test that the probabilities returned by predict_proba are within the valid range [0, 1].

    This test uses a FakePlanetClassifier and checks that all returned probabilities
    are within the expected range.
    """
    with app_container.reset_singletons():
        with app_container.planet_classifier.override(FakePlanetClassifier()):
            planet_classifier = app_container.planet_classifier()
            planet2prob = planet_classifier.predict_proba(sample_image_np)
            for planet, prob in planet2prob.items():
                if prob < 0 or prob > 1:
                    raise AssertionError(f"Probability for planet '{planet}' is out of range: {prob}")
