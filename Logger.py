import logging
import os
from argparse import Namespace
from logging.config import dictConfig


class Logger():
    numeric_level = None
    logger = None

    def __init__(self, parser=None) -> None:
        
        options = None

        if parser:
            options = parser.parse_args()
        else:
            options = Namespace(log='info')

        self.numeric_level = getattr(logging, options.log.upper(), None)

        if not isinstance(self.numeric_level, int):
            raise ValueError('Invalid log level: %s' % self.numeric_level)
        
        self.setup_logging()

    def setup_logging(self, dir=f"{os.path.dirname(os.path.realpath(__file__))}/logs"):
        log_dir = dir

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format':'%(asctime)s -> %(message)s'
                }
            },
            'handlers': {
                'default': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                    'level': self.numeric_level,
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'backupCount': 5,
                    'maxBytes': 5242880,
                    'level': 10,
                    'filename': '{}/app_manager.log'.format(log_dir),
                    'formatter': 'standard'
                }
            },
            "loggers": {
                "logFile": {
                    'handlers': ['default', 'file'],
                    'level': 10 if self.numeric_level < 20 else 20
                }
            }
        }

        dictConfig(config)
        
        self.logger = logging.getLogger('logFile')
