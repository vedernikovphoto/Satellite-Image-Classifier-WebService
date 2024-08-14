from fastapi.testclient import TestClient
from http import HTTPStatus

def test_genres_list(client: TestClient):
    response = client.get('/planet/classes')
    assert response.status_code == HTTPStatus.OK

    classes = response.json()['classes']
    assert isinstance(classes, list)


def test_predict(client: TestClient, sample_image_bytes: bytes):
    files = {
        'image': sample_image_bytes,
    }
    response = client.post('/planet/predict', files=files)

    assert response.status_code == HTTPStatus.OK

    predicted_planets = response.json()['classes']

    assert isinstance(predicted_planets, list)


def test_predict_proba(client: TestClient, sample_image_bytes: bytes):
    files = {
        'image': sample_image_bytes,
    }
    response = client.post('/planet/predict_proba', files=files)

    assert response.status_code == HTTPStatus.OK

    planet2prob = response.json()

    for planet_prob in planet2prob.values():
        assert planet_prob <= 1
        assert planet_prob >= 0
