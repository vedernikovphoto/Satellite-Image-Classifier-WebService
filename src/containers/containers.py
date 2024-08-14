from dependency_injector import containers, providers

from src.services.planet_analysys import PlanetAnalytics
from src.services.planet_classifier import PlanetClassifier


class AppContainer(containers.DeclarativeContainer):
    """
    Dependency Injection container for the application.

    This container holds the configuration and service providers
    for the PlanetClassifier and PlanetAnalytics services. The services
    are provided as singletons, ensuring that only one instance of each
    is created and shared across the application.

    Attributes:
        config (providers.Configuration): A configuration provider that can be
            used to load and manage configuration settings for the services.
        planet_classifier (providers.Singleton): A singleton provider for
            PlanetClassifier, initialized with configuration settings.
        planet_analytics (providers.Singleton): A singleton provider for
            PlanetAnalytics, which depends on PlanetClassifier.
    """

    config = providers.Configuration()

    planet_classifier = providers.Singleton(
        PlanetClassifier,
        config=config.services.planet_classifier,
    )

    planet_analytics = providers.Singleton(
        PlanetAnalytics,
        planet_classifier=planet_classifier,
    )
