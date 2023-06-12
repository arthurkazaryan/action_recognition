from pathlib import Path
from typing import NoReturn

import requests
import tarfile

from settings import KINETICS_DATASET_URL


class DatasetPathsData(object):
    class KineticsPathsData(object):
        def __init__(self, native: Path) -> None:
            self.native = native
            self.train = native.joinpath("train.csv")
            self.val = native.joinpath("validate.csv")
            self.test = native.joinpath("test.csv")

    def __init__(self) -> None:
        self.native = Path("datasets")
        self.native.mkdir(parents=True, exist_ok=True)
        self.archive_path: Path = self.native.joinpath("kinetics700.tar.gz")
        self.archive_folder = self.KineticsPathsData(self.native.joinpath("kinetics700"))

    def download_dataset(self) -> NoReturn:
        response = requests.get(KINETICS_DATASET_URL)
        with open(self.archive_path, "wb") as archive:
            archive.write(response.content)

    def extract_dataset(self) -> NoReturn:
        archive_file = tarfile.open(self.archive_path)
        archive_file.extractall(self.native)
        archive_file.close()
