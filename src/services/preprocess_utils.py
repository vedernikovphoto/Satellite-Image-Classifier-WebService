import typing as tp

import cv2
import numpy as np
import torch


MAX_PIXEL_VALUE = 255.0


def preprocess_image(image: np.ndarray, target_image_size: tp.Tuple[int, int]) -> torch.Tensor:
    """
    Preprocesses an image for input into a neural network.

    This function normalizes the input image, resizes it to the target size,
    adjusts the color channels, and converts the image into a format suitable
    for input into a deep learning model.

    Args:
        image (np.ndarray): The input RGB image as a NumPy array.
        target_image_size (tp.Tuple[int, int]): The desired (width, height) size of the image.

    Returns:
        torch.Tensor: A tensor representing the preprocessed image, with dimensions
                      (1, 3, height, width) where height and width are specified
                      by `target_image_size`.
    """
    image = image.astype(np.float32)
    image /= MAX_PIXEL_VALUE
    image = cv2.resize(image, target_image_size)
    image = np.transpose(image, (2, 0, 1))
    image -= np.array([0.485, 0.456, 0.406])[:, None, None]
    image /= np.array([0.229, 0.224, 0.225])[:, None, None]
    return torch.from_numpy(image)[None]
