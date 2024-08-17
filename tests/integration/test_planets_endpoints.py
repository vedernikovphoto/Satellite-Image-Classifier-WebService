from fastapi.testclient import TestClient
from http import HTTPStatus


def test_genres_list(client: TestClient):
    response = client.get('/planet/classes')
    if response.status_code != HTTPStatus.OK:
        raise AssertionError(f'Expected status {HTTPStatus.OK}, got {response.status_code}')

    classes = response.json()['classes']
    if not isinstance(classes, list):
        raise AssertionError(f"Expected 'classes' to be a list, got {type(classes)}")


def test_predict(client: TestClient, sample_image_bytes: bytes):
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
