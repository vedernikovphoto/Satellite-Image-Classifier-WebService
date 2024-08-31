from dependency_injector import containers, providers

from src.services.planet_classifier import PlanetClassifier


class AppContainer(containers.DeclarativeContainer):
    """
    Dependency Injection container for the application.

    This container provides and configures the services
    for PlanetClassifier and PlanetAnalytics.

    Attributes:
        config (providers.Configuration): Configuration settings for the services.
        planet_classifier (providers.Singleton): Provides the PlanetClassifier service.
        planet_analytics (providers.Singleton): Provides the PlanetAnalytics service, dependent on PlanetClassifier.
    """

    config = providers.Configuration()

    planet_classifier = providers.Singleton(
        PlanetClassifier,
        config=config.services.planet_classifier,
    )
