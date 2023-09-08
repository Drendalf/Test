import sys
import time

from flask import Flask
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import InitDataError
from ..logs import logger
from ..models.model import db
from ..models.model import Itcompanies


DB_MODELS = (Itcompanies,)
TOTAL_ATTEMPTS = 30
FIRST_COMPANY_PAYLOAD = {
    "name_company": "test",
    "code_okved": "test",
    "inn": 11111,
    "kpp": 11111,
    "place_of_registration": "test",
}


def _load_first_company() -> None:
    try:
        new_obj = Itcompanies(**FIRST_COMPANY_PAYLOAD)
        db.session.add(new_obj)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InitDataError(
            f'Load init data | error load {FIRST_COMPANY_PAYLOAD["name_company"]} '
        )


def load_init_data():
    _load_first_company()


def db_init(app: Flask) -> Flask:
    # Create tables in database.
    with app.app_context():
        for attempt in range(TOTAL_ATTEMPTS):
            logger.info(
                f"Database initialization attempt ({attempt}/{TOTAL_ATTEMPTS})!"
            )

            try:
                db.session.execute(text("SELECT version();"))
            except OperationalError as e:
                logger.error(f"Database not available: {e}!")
                time.sleep(1)
                continue

            try:
                db.create_all()
            except SQLAlchemyError as e:
                logger.error(f"Database not created: {repr(e)}!")
                time.sleep(1)
                continue

            db_empty = True
            for model in DB_MODELS:
                one_record = db.session.scalar(select(model))
                if one_record:
                    db_empty = False
                    break
            if db_empty:
                try:
                    load_init_data()
                    break
                except InitDataError as e:
                    logger.error(f"Tables not filled: {repr(e)}!")
            break

        else:
            sys.exit()

    return app
