import numpy as np

from typing import Dict, List
from src.services.planet_classifier import PlanetClassifier


class PlanetAnalytics:
    """
    A class to perform analytics on planet images using a classifier.

    This class provides methods to predict the class of a planet image and
    to obtain the probability distribution over possible planet classes.
    """

    def __init__(self, planet_classifier: PlanetClassifier):
        """
        Initializes the PlanetAnalytics with a given PlanetClassifier.

        :param planet_classifier: An instance of PlanetClassifier used to predict planet classes.
        """
        self._planet_classifier = planet_classifier

    @property
    def classes(self):
        """Returns the list of possible planet classes."""
        return self._planet_classifier.classes

    def predict(self, image: np.ndarray) -> List[str]:
        """Predicts the classes for a planet image.

        :param image: Input RGB image;
        :return: List of planet classes.
        """
        return self._planet_classifier.predict(image)

    def predict_proba(self, image: np.ndarray) -> Dict[str, float]:
        """Predicts the probabilities for each planet class.

        :param image: Input RGB image;
        :return: Dictionary with planet class as key and probability as value.
        """
        return self._planet_classifier.predict_proba(image)
