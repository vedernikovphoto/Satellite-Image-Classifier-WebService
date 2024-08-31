import typing as tp
import numpy as np
import torch

from src.services.preprocess_utils import preprocess_image


class PlanetClassifier:
    """
    A classifier for predicting planet classes from images using a pre-trained PyTorch model.

    Attributes:
        _cfg (dict): Configuration dictionary with keys 'model_path', 'device', 'classes',
        'input_size', and 'thresholds'.
        _model (torch.jit.ScriptModule): Loaded PyTorch model.
    """

    def __init__(self, config: tp.Dict):
        """
        Initializes the PlanetClassifier with a configuration dictionary.

        :param cfg: Dictionary containing model path, device, classes, input size, and thresholds.
        """
        self._cfg = config

        model_path = self._cfg['model_path']
        device = torch.device(self._cfg['device'])
        self._model = torch.jit.load(model_path, map_location=device)

        self._model.to(self._cfg['device'])
        self._model.eval()

    @property
    def classes(self) -> tp.List[str]:
        """
        Returns the list of planet classes.

        :return: List of planet classes.
        """
        return list(self._cfg['classes'])

    @property
    def size(self) -> tp.Tuple:
        """
        Returns the input size of the images.

        :return: Tuple representing the width and height of the input image.
        """
        return self._cfg['input_size']

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
        batch = preprocess_image(image, self._cfg['input_size'])
        classes = self._cfg['classes']


        with torch.no_grad():
            batch_device = batch.to(self._cfg['device'])
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

        :param image: RGB image as a NumPy array.
        :return: NumPy array of predicted probabilities.
        """
        batch = preprocess_image(image, self._cfg['input_size'])

        with torch.no_grad():
            batch_on_device = batch.to(self._cfg['device'])
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
        classes = self._cfg['classes']
        thresholds = self._cfg['thresholds']
        
        for i, _ in enumerate(classes):
            if predict[i] > thresholds:
                selected_classes.append(classes[i])
        return selected_classes

    def _postprocess_predict_proba(self, predict: np.ndarray) -> tp.Dict[str, float]:
        """
        Post-processes the predicted probabilities to obtain a dictionary of class probabilities.

        :param predict: NumPy array of predicted probabilities.
        :return: Dictionary mapping each planet class to its probability.
        """

        classes = self._cfg['classes']

        sorted_indices = predict.argsort()[::-1]
        return {
            classes[int(i)]: float(predict[i])
            for i in sorted_indices
        }
