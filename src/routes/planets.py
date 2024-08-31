import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, File

from src.containers.containers import AppContainer
from src.routes.routers import router
from src.services.planet_analysys import PlanetAnalytics


@router.get('/classes')
@inject
def classes_list(service: PlanetAnalytics = Depends(Provide[AppContainer.planet_analytics])):
    """
    Get the list of available classes.

    Args:
        service (PlanetAnalytics): Injected PlanetAnalytics service.

    Returns:
        dict: Available classes for prediction.
    """
    return {
        'classes': service.classes,
    }


@router.post('/predict')
@inject
def predict(
    image: bytes = File(...),
    service: PlanetAnalytics = Depends(Provide[AppContainer.planet_analytics]),
):
    """
    Predict the class of the input image.

    Args:
        image (bytes): Uploaded image file.
        service (PlanetAnalytics): Injected PlanetAnalytics service.

    Returns:
        dict: Predicted class for the image.
    """
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    classes = service.predict(img)

    return {'classes': classes}


@router.post('/predict_proba')
@inject
def predict_proba(
    image: bytes = File(...),
    service: PlanetAnalytics = Depends(Provide[AppContainer.planet_analytics]),
):
    """
    Predict class probabilities for the input image.

    Args:
        image (bytes): Uploaded image file.
        service (PlanetAnalytics): Injected PlanetAnalytics service.

    Returns:
        dict: Predicted probabilities for each class.
    """
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    return service.predict_proba(img)
