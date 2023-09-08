import fnmatch
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import Session

from ..extensions import db
from ..logs import logger
from ..models.model import Itcompanies

CITY_PATTERN = "Хабаровск"
OKVED_PATTERN = "62"
FILE_PATTERN = "*.json"
ARCHIVE_NAME = "egrul.json.zip"


def sample_org():
    temporary_files_path = os.path.join("temp", "egrul.json")
    result = []

    with ZipFile("egrul.json.zip", mode="r") as zf:
        for file in zf.infolist():
            name = os.path.basename(file.filename)
            file_temporary_files_path = os.path.join(temporary_files_path, name)

            if fnmatch.fnmatch(name, FILE_PATTERN):
                zf.extract(file.filename, "temp")

                with open(file_temporary_files_path, "rb") as data:
                    for el in json.load(data):
                        try:
                            okved = el["data"]["СвОКВЭД"]["СвОКВЭДОсн"]["КодОКВЭД"][0:2]
                            adres = el["data"]["СвРегОрг"]["АдрРО"]

                            if okved == OKVED_PATTERN and adres == CITY_PATTERN:
                                data = {
                                    "name_company": el["name"],
                                    "inn": el["inn"],
                                    "kpp": el["kpp"],
                                    "place_of_registration": el["data"]["СвРегОрг"][
                                        "АдрРО"
                                    ],
                                }
                                result.append(data)

                        except KeyError as ex:
                            logger.debug(f'{el["name"]} неуказан {ex}')

    return result


class SafeController:
    BASE_DIR = Path().absolute()
    TEMP_FILES_PATH = Path(BASE_DIR, "temp")
    ARCHIVE_URL = f"https://ofdata.ru/open-data/download/{ARCHIVE_NAME}"
    ARCHIVE_PATH = Path(BASE_DIR, ARCHIVE_NAME)
    DOWNLOAD_NUMBER_OF_ATTEMPTS = 10

    def __init__(self, model: DeclarativeMeta, session: Session) -> None:
        self._model = model
        self.db_session = session

    def archive_download(self):
        logger.debug(f"{datetime.utcnow()} | Загрузка архива")

        subprocess.run(
            [
                "wget",
                "--continue",
                "--tries",
                str(self.DOWNLOAD_NUMBER_OF_ATTEMPTS),
                "--directory-prefix",
                os.path.split(self.ARCHIVE_PATH)[0],
                self.ARCHIVE_URL,
            ],
            stdout=subprocess.PIPE,
        )

        logger.debug(f"{datetime.utcnow()} | Архив загружен")

    def create_company(self, data):
        new_obj = Itcompanies(**data)
        db.session.add(new_obj)
        db.session.commit()
