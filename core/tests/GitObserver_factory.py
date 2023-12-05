from GitObserver import GitObserver
from core.tests.config_factory import ConfigFactory


class GitObserverFactory:

    @staticmethod
    def create_default() -> GitObserver:
        """
        Loads default configuration from ConfigFactory
        and creates a test instance of GitObserver using it
        :return: test instance of GitObserver
        """
        config = ConfigFactory.create_defaults()
        observer = GitObserver(config, is_test_instance=True)
        return observer
