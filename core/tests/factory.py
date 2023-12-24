import pathlib
from datetime import datetime

from observer import GitObserver
from core.config.management import ConfigManager
import core.paths
import core.unittestutils


c_paths = core.paths.Paths()
ut_utils = core.unittestutils.UTUtils()


class GitObserverFactory:

    @staticmethod
    def create_default() -> GitObserver:
        """
        Loads default configuration from ConfigFactory
        and creates a test instance of GitObserver using it
        :return: test instance of GitObserver
        """
        config = ConfigManager.get_defaults()
        observer = GitObserver(config, is_test_instance=True)
        return observer


class LoggerFactory:
    @staticmethod
    def create_log_file_path() -> pathlib.Path:
        dt_now: datetime = datetime.now()
        date_initial_strf: str = dt_now.strftime('%Y-%m-%d')
        log_dir: pathlib.Path = c_paths.LOG_DIR
        log_file: pathlib.Path = ut_utils.lazy_path_obj(f'log_{date_initial_strf}.log')
        return log_dir / log_file


class UtilsFactory:
    @staticmethod
    def create_bunny_file(fp: str | pathlib.Path):
        bunny = r"""
               ((`\
            ___ \\ '--._
         .'`   `'    o  )
        /    \   '. __.'
       _|    /_  \ \_\_
jgs   {_\______\-'\__\_\
"""
        file = ut_utils.lazy_path_obj(fp)

        with open(file, 'w+', encoding='utf8') as f:
            f.write(bunny)


class EnvCheckFactory:
    @staticmethod
    def convert_list_to_dict(_list) -> dict:
        _dict: dict = {}
        for x in _list:
            _dict.update({x: 'Test'})
        return _dict
