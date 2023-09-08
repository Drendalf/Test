from logging import getLogger
from logging.config import dictConfig

from .config import Config

dictConfig(Config.LOGGING_CONFIG)

logger = getLogger(Config.APP_NAME)
