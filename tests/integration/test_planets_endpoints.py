from fastapi.testclient import TestClient
from http import HTTPStatus


def test_genres_list(client: TestClient):
    """
    Test the endpoint that returns a list of planet classes.
    Verifies that the response status is OK and that the returned classes are a list.
    """
    response = client.get('/planet/classes')
    if response.status_code != HTTPStatus.OK:
        raise AssertionError(f'Expected status {HTTPStatus.OK}, got {response.status_code}')

    classes = response.json()['classes']
    if not isinstance(classes, list):
        raise AssertionError(f"Expected 'classes' to be a list, got {type(classes)}")


def test_predict(client: TestClient, sample_image_bytes: bytes):
    """
    Test the endpoint that predicts planet classes from an image.
    Verifies that the response status is OK and that the returned classes are a list.
    """
    files = {
        'image': sample_image_bytes,
    }
    response = client.post('/planet/predict', files=files)

    if response.status_code != HTTPStatus.OK:
        raise AssertionError(f'Expected status {HTTPStatus.OK}, got {response.status_code}')

    predicted_planets = response.json()['classes']
    if not isinstance(predicted_planets, list):
        raise AssertionError(f"Expected 'classes' to be a list, got {type(predicted_planets)}")


def test_predict_proba(client: TestClient, sample_image_bytes: bytes):
    """
    Test the endpoint that predicts the probability distribution over planet classes from an image.
    Verifies that the response status is OK and that the probabilities are within the valid range [0, 1].
    """
    files = {
        'image': sample_image_bytes,
    }
    response = client.post('/planet/predict_proba', files=files)

    if response.status_code != HTTPStatus.OK:
        raise AssertionError(f'Expected status {HTTPStatus.OK}, got {response.status_code}')

    planet2prob = response.json()

    for planet, prob in planet2prob.items():
        if prob < 0 or prob > 1:
            raise AssertionError(f"Probability for planet '{planet}' is out of range: {prob}")
