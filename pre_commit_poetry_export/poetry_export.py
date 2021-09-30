import hashlib
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryFile


def get_checksum(requirements: str):
    """Determine the hash from the contents of the requirements."""
    hash_ = hashlib.md5()
    hash_.update(requirements.encode('utf-8'))
    return hash_.hexdigest()


def main(argv=None):
    requirements_path = Path('requirements.txt')

    if not requirements_path.exists():
        with open(requirements_path, "w") as requirements_file:
            subprocess.run(
                ['poetry', 'export', '-f', 'requirements.txt'],
                stdout=requirements_file,
                text=True,
            )
        print('requirements.txt created')
        return 1

    with open(requirements_path, "r") as requirements_file:
        current_hash = get_checksum(requirements_file.read())

    with TemporaryFile("w+") as tmp_requirements:
        subprocess.run(
            ['poetry', 'export', '-f', 'requirements.txt'],
            stdout=tmp_requirements,
            text=True,
        )
        tmp_requirements.seek(0)
        new_requirements = tmp_requirements.read()
        new_hash = get_checksum(new_requirements)

        if current_hash == new_hash:
            return 0

    with open(requirements_path, "w") as requirements_file:
        requirements_file.write(new_requirements)

    print('requirements.txt updated!')
    return 2


if __name__ == '__name__':
    sys.exit(main())
