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
    """
    Fixture to provide a sample image as bytes.

    Reads a sample image file from the 'images' directory and yields its contents as bytes.
    """
    with open(os.path.join(TESTS_DIR, 'images', 'file_99.jpg'), 'rb') as image_file:
        yield image_file.read()


@pytest.fixture
def sample_image_np():
    """
    Fixture to provide a sample image as a NumPy array.

    Reads a sample image file, converts it from BGR to RGB format, and returns it as a NumPy array.
    """
    img = cv2.imread(os.path.join(TESTS_DIR, 'images', 'file_99.jpg'))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


@pytest.fixture(scope=SESSION_SCOPE)
def app_config():
    """
    Fixture to provide the application configuration.

    Loads the configuration from '/project_root_folder/config/config.yml' using OmegaConf.
    """
    return OmegaConf.load(os.path.join(TESTS_DIR, '..', 'config', 'config.yml'))


@pytest.fixture(scope=SESSION_SCOPE)
def app_container(app_config):
    """
    Fixture to provide an AppContainer instance configured with the test configuration.

    Returns an instance of AppContainer with its configuration loaded from the test config.
    """
    container = AppContainer()
    container.config.from_dict(app_config)
    return container


@pytest.fixture(scope=SESSION_SCOPE)
def wired_app_container(app_config):
    """
    Fixture to provide a wired AppContainer instance.

    Configures and wires the AppContainer for use with FastAPI routes. Unwires the container after the test session.
    """
    container = AppContainer()
    container.config.from_dict(app_config)
    container.wire([planet_routes])
    logger.info('start')
    yield
    container.unwire()


@pytest.fixture(scope=SESSION_SCOPE)
def test_app(wired_app_container):
    """
    Fixture to provide the FastAPI application instance.

    Returns the FastAPI app instance for use in tests.
    """
    return app


@pytest.fixture(scope=SESSION_SCOPE)
def client(test_app):
    """
    Fixture to provide a test client for the FastAPI application.

    Returns a TestClient instance for making requests to the FastAPI app in tests.
    """
    return TestClient(test_app)
