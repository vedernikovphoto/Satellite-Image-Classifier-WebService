import typing as tp
import numpy as np
import torch

from src.services.preprocess_utils import preprocess_image


class PlanetClassifier:
    """
    A classifier for predicting planet classes from images using a pre-trained PyTorch model.

    Attributes:
        model (torch.jit.ScriptModule): The loaded PyTorch model.
        device (torch.device): The device on which the model is running.
        input_size (Tuple[int, int]): The expected input size of images.
        classes (List[str]): The list of planet classes.
        thresholds (Dict[str, float]): Thresholds for each class to determine if it is predicted.
    """

    def __init__(self, config: tp.Dict):
        """
        Initializes the PlanetClassifier with a configuration dictionary.

        Args:
            config (dict): Dictionary containing model path, device, classes, input size, and thresholds.
        """
        self._cfg = config
        self.device_key = 'device'
        self.classes_key = 'classes'
        model_path = self._cfg['model_path']
        device = torch.device(self._cfg[self.device_key])
        self._model = torch.jit.load(model_path, map_location=device)

        self._model.to(self._cfg[self.device_key])
        self._model.eval()

    @property
    def classes(self) -> tp.List[str]:
        """
        Returns the list of planet classes.

        Returns:
            List[str]: A list of planet classes.
        """
        return list(self._cfg[self.classes_key])

    @property
    def size(self) -> tp.Tuple[int, int]:
        """
        Returns the input size of the images.

        Returns:
            Tuple[int, int]: The width and height of the input image.
        """
        return self._cfg['input_size']

    def predict(self, image: np.ndarray) -> tp.List[str]:
        """
        Predicts planet classes for the given image.

        Args:
            image (np.ndarray): RGB image as a NumPy array.

        Returns:
            List[str]: A list of predicted planet classes.
        """
        return self._postprocess_predict(self._predict(image))

    def predict_proba(self, image: np.ndarray) -> tp.Dict[str, float]:
        """
        Predicts the probabilities of planet classes for the given image.

        Args:
            image (np.ndarray): RGB image as a NumPy array.

        Returns:
            Dict[str, float]: A dictionary mapping each planet class to its probability.
        """
        batch = preprocess_image(image, self._cfg['input_size'])
        classes = self._cfg[self.classes_key]

        with torch.no_grad():
            batch_device = batch.to(self._cfg[self.device_key])
            model_output = self._model(batch_device)
            logits = model_output.detach().cpu()[0]
            probabilities = torch.sigmoid(torch.tensor(logits)).numpy()

        class_probabilities = {}
        for i, _ in enumerate(classes):
            class_name = classes[int(i)]
            probability = round(float(probabilities[i]), 4)
            class_probabilities[class_name] = probability
        return class_probabilities

    def _predict(self, image: np.ndarray) -> np.ndarray:
        """
        Runs the model to predict probabilities for the given image.

        Args:
            image (np.ndarray): RGB image as a NumPy array.

        Returns:
            np.ndarray: Array of predicted probabilities.
        """
        batch = preprocess_image(image, self._cfg['input_size'])

        with torch.no_grad():
            batch_on_device = batch.to(self._cfg[self.device_key])
            model_output = self._model(batch_on_device)
            model_predict = model_output.detach().cpu()[0]

        return model_predict.numpy()

    def _postprocess_predict(self, predict: np.ndarray) -> tp.List[str]:
        """
        Post-processes the predicted probabilities to obtain a list of planet classes.

        Args:
            predict (np.ndarray): Array of predicted probabilities.

        Returns:
            List[str]: A list of predicted planet classes based on the thresholds.
        """
        selected_classes = []
        classes = self._cfg[self.classes_key]
        thresholds = self._cfg['thresholds']

        for i, _ in enumerate(classes):
            if predict[i] > thresholds:
                selected_classes.append(classes[i])
        return selected_classes

    def _postprocess_predict_proba(self, predict: np.ndarray) -> tp.Dict[str, float]:
        """
        Post-processes the predicted probabilities to obtain a dictionary of class probabilities.

        Args:
            predict (np.ndarray): Array of predicted probabilities.

        Returns:
            Dict[str, float]: A dictionary mapping each planet class to its probability.
        """
        classes = self._cfg[self.classes_key]

        sorted_indices = predict.argsort()[::-1]
        return {
            classes[int(i)]: float(predict[i])
            for i in sorted_indices
        }
