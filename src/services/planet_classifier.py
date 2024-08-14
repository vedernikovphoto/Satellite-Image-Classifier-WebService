import typing as tp
import numpy as np
import torch

from src.services.preprocess_utils import preprocess_image


class PlanetClassifier:
    """
    A classifier for predicting planet classes from images using a pre-trained PyTorch model.

    Attributes:
        config (dict): Configuration dictionary with keys 'model_path', 'device', 'classes',
        'input_size', and 'thresholds'.
        _model_path (str): Path to the serialized PyTorch model.
        _device (str): Device to run the model on ('cpu' or 'cuda').
        _classes (List[str]): List of possible planet classes.
        _size (Tuple[int, int]): Input size for images.
        _thresholds (float or List[float]): Threshold(s) for classifying planets.
        _model (torch.jit.ScriptModule): Loaded PyTorch model.
    """

    def __init__(self, config: dict):
        """
        Initializes the PlanetClassifier with a configuration dictionary.

        :param config: Dictionary containing model path, device, classes, input size, and thresholds.
        """
        self._model_path = config['model_path']
        self._device = config['device']
        self._classes = config.get('classes', [])
        self._size = config.get('input_size', [224, 224])
        self._thresholds = config.get('thresholds', 0.5)

        model_path = self._model_path
        device = torch.device(self._device)
        self._model = torch.jit.load(model_path, map_location=device)

        self._model.to(self._device)
        self._model.eval()

    @property
    def classes(self) -> tp.List:
        """
        Returns the list of planet classes.

        :return: List of planet classes.
        """
        return list(self._classes)

    @property
    def size(self) -> tp.Tuple:
        """
        Returns the input size of the images.

        :return: Tuple representing the width and height of the input image.
        """
        return self._size

    def predict(self, image: np.ndarray) -> tp.List[str]:
        """
        Predicts planet classes for the given image.

        :param image: RGB image as a NumPy array.
        :return: List of predicted planet classes.
        """
        return self._postprocess_predict(self._predict(image))

    def predict_proba(self, image: np.ndarray) -> tp.Dict[str, float]:
        """
        Predicts the probabilities of planet classes for the given image.

        :param image: RGB image as a NumPy array.
        :return: Dictionary mapping each planet class to its probability.
        """
        batch = preprocess_image(image, self._size)

        with torch.no_grad():
            batch_device = batch.to(self._device)
            model_output = self._model(batch_device)
            logits = model_output.detach().cpu()[0]
            probabilities = torch.sigmoid(torch.tensor(logits)).numpy()

        class_probabilities = {}
        for i, _ in enumerate(self._classes):
            class_name = self._classes[int(i)]
            probability = round(float(probabilities[i]), 4)
            class_probabilities[class_name] = probability
        return class_probabilities

    def _predict(self, image: np.ndarray) -> np.ndarray:
        """
        Runs the model to predict probabilities for the given image.

        :param image: RGB image as a NumPy array.
        :return: NumPy array of predicted probabilities.
        """
        batch = preprocess_image(image, self._size)

        with torch.no_grad():
            batch_on_device = batch.to(self._device)
            model_output = self._model(batch_on_device)
            model_predict = model_output.detach().cpu()[0]

        return model_predict.numpy()

    def _postprocess_predict(self, predict: np.ndarray) -> tp.List[str]:
        """
        Post-processes the predicted probabilities to obtain a list of planet classes.

        :param predict: NumPy array of predicted probabilities.
        :return: List of predicted planet classes based on the thresholds.
        """
        selected_classes = []
        for i, _ in enumerate(self._classes):
            if predict[i] > self._thresholds:
                selected_classes.append(self._classes[i])
        return selected_classes

    def _postprocess_predict_proba(self, predict: np.ndarray) -> tp.Dict[str, float]:
        """
        Post-processes the predicted probabilities to obtain a dictionary of class probabilities.

        :param predict: NumPy array of predicted probabilities.
        :return: Dictionary mapping each planet class to its probability.
        """
        sorted_indices = predict.argsort()[::-1]
        return {
            self._classes[int(i)]: float(predict[i])
            for i in sorted_indices
        }
