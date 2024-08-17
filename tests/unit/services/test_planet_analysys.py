import numpy as np
from src.containers.containers import AppContainer


class FakePlanetClassifier:

    def predict(self, image):
        return []

    def predict_proba(self, image):
        return {'value': 0.2}


def test_predicts_not_fail(app_container: AppContainer, sample_image_np: np.ndarray):
    with app_container.reset_singletons():
        with app_container.planet_classifier.override(FakePlanetClassifier()):
            planet_analytics = app_container.planet_analytics()
            planet_analytics.predict(sample_image_np)
            planet_analytics.predict_proba(sample_image_np)


def test_prob_less_or_equal_to_one(app_container: AppContainer, sample_image_np: np.ndarray):
    with app_container.reset_singletons():
        with app_container.planet_classifier.override(FakePlanetClassifier()):
            planet_analytics = app_container.planet_analytics()
            planet2prob = planet_analytics.predict_proba(sample_image_np)
            for planet, prob in planet2prob.items():
                if prob < 0 or prob > 1:
                    raise AssertionError(f"Probability for planet '{planet}' is out of range: {prob}")
