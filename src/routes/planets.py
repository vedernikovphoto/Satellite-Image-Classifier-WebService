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
    Endpoint to get the list of available classes.

    Args:
        service (PlanetAnalytics): The PlanetAnalytics service injected by dependency injection.

    Returns:
        dict: A dictionary containing the list of classes available for prediction.
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
    Endpoint to predict the class of the input image.

    Args:
        image (bytes): The image file uploaded by the user.
        service (PlanetAnalytics): The PlanetAnalytics service injected by dependency injection.

    Returns:
        dict: A dictionary containing the predicted class for the image.
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
    Endpoint to predict the class probabilities for the input image.

    Args:
        image (bytes): The image file uploaded by the user.
        service (PlanetAnalytics): The PlanetAnalytics service injected by dependency injection.

    Returns:
        dict: A dictionary containing the predicted probabilities for each class.
    """
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    return service.predict_proba(img)
