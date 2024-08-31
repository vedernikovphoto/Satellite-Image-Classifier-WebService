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

        Args:
            planet_classifier (PlanetClassifier): The classifier used to predict planet classes.
        """
        self._planet_classifier = planet_classifier

    @property
    def classes(self) -> List[str]:
        """Returns the list of possible planet classes.

        Returns:
            List[str]: A list of possible planet classes.
        """
        return self._planet_classifier.classes

    def predict(self, image: np.ndarray) -> List[str]:
        """Predicts the classes for a planet image.

        Args:
            image (np.ndarray): Input RGB image.

        Returns:
            List[str]: A list of predicted planet classes.
        """
        return self._planet_classifier.predict(image)

    def predict_proba(self, image: np.ndarray) -> Dict[str, float]:
        """Predicts the probabilities for each planet class.

        Args:
            image (np.ndarray): Input RGB image.

        Returns:
            Dict[str, float]: A dictionary with the planet class as the key and the probability as the value.
        """
        return self._planet_classifier.predict_proba(image)
