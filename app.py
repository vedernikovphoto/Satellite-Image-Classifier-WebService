import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from omegaconf import OmegaConf

from src.containers.containers import AppContainer
from src.routes.routers import router as app_router
from src.routes import planets as planet_routes


DEFAULT_PORT = 2444


def root() -> HTMLResponse:
    """
    The root endpoint that returns an HTML response.

    This function generates a simple HTML page with a welcome message
    and a link to the API documentation.

    Returns:
        HTMLResponse: A response containing the generated HTML content.
    """
    html_content = [
        '<html>',
        '    <head>',
        '        <title>Welcome to My API</title>',
        '    </head>',
        '    <body>',
        '        <h1>Welcome to My API</h1>',
        '        <p>Visit <a href=\"/docs\">/docs</a> for the API documentation.</p>',
        '    </body>',
        '</html>',
    ]
    return HTMLResponse('\n'.join(html_content))


def create_app() -> FastAPI:
    """
    Creates and configures an instance of the FastAPI application.

    This function sets up the dependency injection container, loads the configuration,
    wires dependencies, and includes the API routes.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    container = AppContainer()
    cfg = OmegaConf.load('config/config.yml')
    container.config.from_dict(cfg)
    container.wire([planet_routes])

    app = FastAPI()

    app.get('/', response_class=HTMLResponse)(root)

    app.include_router(app_router, prefix='/planet', tags=['planet'])  # Updated prefix and tags

    return app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=DEFAULT_PORT)
