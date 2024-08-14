import random
from copy import deepcopy

import cv2
import numpy as np

from src.containers.containers import AppContainer


class FakePlanetClassifier:

    def predict(self, image):
        return []

    def predict_proba(self, image):
        return dict(value=0.2)


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
            for prob in planet2prob.values():
                assert prob <= 1
                assert prob >= 0


def test_prob_less_or_equal_to_one(app_container: AppContainer, sample_image_np: np.ndarray):
    with app_container.reset_singletons():
        with app_container.planet_classifier.override(FakePlanetClassifier()):
            planet_analytics = app_container.planet_analytics()
            planet2prob = planet_analytics.predict_proba(sample_image_np)
            for prob in planet2prob.values():
                assert prob <= 1
                assert prob >= 0