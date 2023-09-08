import os
from pathlib import Path


basedir = Path().absolute()


class Config:
    DEBUG = os.environ["DEBUG"] == "True"
    ENV = os.environ["ENV"]

    APP_NAME = "test"

    HOST = os.environ["HOST"]
    PORT = int(os.environ["PORT"])

    BASE_DIR = basedir

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "class": "logging.Formatter",
                "format": '{"date_time": "%(asctime)s",'
                ' "microservice": "test",'
                ' "level": "%(levelname)s",'
                ' "message": "%(message)s"}',
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            APP_NAME: {"level": "DEBUG" if DEBUG else "INFO", "handlers": ["console"]},
        },
    }

    # Настройки базы данных.
    # 'postgresql://username:password@host:port/db_name'
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://"
        f'{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}'
        f'@{os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}'
        f'/{os.environ["POSTGRES_DB"]}'
    )

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False