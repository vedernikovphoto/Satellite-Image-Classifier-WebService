import os
import cv2
import pytest
import logging
from fastapi.testclient import TestClient
from omegaconf import OmegaConf

from app import app
from src.containers.containers import AppContainer
from src.routes import planets as planet_routes

TESTS_DIR = os.path.dirname(__file__)
SESSION_SCOPE = 'session'
logger = logging.getLogger(__name__)


@pytest.fixture(scope=SESSION_SCOPE)
def sample_image_bytes():
    f = open(os.path.join(TESTS_DIR, 'images', 'file_99.jpg'), 'rb')  # noqa: WPS515
    try:
        yield f.read()
    finally:
        f.close()


@pytest.fixture
def sample_image_np():
    img = cv2.imread(os.path.join(TESTS_DIR, 'images', 'file_99.jpg'))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


@pytest.fixture(scope=SESSION_SCOPE)
def app_config():
    return OmegaConf.load(os.path.join(TESTS_DIR, 'test_config.yml'))


@pytest.fixture(scope=SESSION_SCOPE)
def app_container(app_config):
    container = AppContainer()
    container.config.from_dict(app_config)
    return container


@pytest.fixture(scope=SESSION_SCOPE)
def wired_app_container(app_config):
    container = AppContainer()
    container.config.from_dict(app_config)
    container.wire([planet_routes])
    logger.info('start')
    yield
    container.unwire()


@pytest.fixture(scope=SESSION_SCOPE)
def test_app(wired_app_container):
    return app


@pytest.fixture(scope=SESSION_SCOPE)
def client(test_app):
    return TestClient(test_app)
