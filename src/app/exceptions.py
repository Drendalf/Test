from flask import Flask
from sqlalchemy.exc import IntegrityError

from .extensions import db
from .logs import logger


class InitDataError(Exception):
    """Exception if error of init data."""


def register_errors(app: Flask) -> Flask:
    """Registering handlers for all errors."""

    @app.errorhandler(IntegrityError)
    def obj_exist_exception(exc) -> tuple:
        """Exception handler for exist unique object in db."""
        logger.debug(repr(exc))
        db.session.rollback()
        return {
            "code": 422,
            "name": "Unprocessable Entity",
            "description": "Object exists.",
        }, 422

    return app