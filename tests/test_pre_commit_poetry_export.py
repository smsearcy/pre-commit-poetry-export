import os
from pathlib import Path
from shutil import copy

from pre_commit_poetry_export.poetry_export import main


def populate_tmp_data_path(tmp_path: Path, folder: str):
    """Returns a temporary directory, populated with data for our test."""
    data_path = Path(__file__).parent / "data" / folder
    for data_file in data_path.iterdir():
        copy(data_file, tmp_path)


def test_requirements_current(tmp_path):
    populate_tmp_data_path(tmp_path, "requirements-current")
    os.chdir(tmp_path)

    # no changes should result in 0 return code
    assert main() == 0


def test_requirements_missing(tmp_path):
    populate_tmp_data_path(tmp_path, "requirements-missing")
    os.chdir(tmp_path)

    # first time should detect missing
    assert main() != 0
    # second time should be good
    assert main() == 0


def test_requirements_out_of_date(tmp_path):
    populate_tmp_data_path(tmp_path, "requirements-out-of-date")
    os.chdir(tmp_path)

    # first time should detect out of date
    assert main() != 0
    # second time should be good
    assert main() == 0
