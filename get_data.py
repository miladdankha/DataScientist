"""Fetch the two verified public survey files. Existing valid files are reused."""
from hashlib import file_digest
from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

DATA = Path(__file__).resolve().parent / "data"
ANSWERS = DATA / "survey_results_public.csv"
SCHEMA = DATA / "survey_results_schema.csv"
BASE_URL = "https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2026/"
DIGESTS = {
    ANSWERS.name: "ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c",
    SCHEMA.name: "0892967cacdac5cdd1a7668de6f5edd8947bcc0ab204b7ec3e2d81084eb00b63",
}


def checksum(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def fetch(directory=DATA):
    directory.mkdir(parents=True, exist_ok=True)
    for name, expected in DIGESTS.items():
        target = directory / name
        if target.is_file() and checksum(target) == expected:
            print(f"Verified: {name}")
            continue
        with NamedTemporaryFile(dir=directory, delete=False) as tmp:
            staging = Path(tmp.name)
        try:
            with urlopen(BASE_URL + name, timeout=120) as response, staging.open("wb") as out:
                copyfileobj(response, out)
            if checksum(staging) != expected:
                raise ValueError(f"Unexpected SHA-256 checksum for {name}. Check the official release.")
            staging.replace(target)
            print(f"Downloaded and verified: {name}")
        finally:
            staging.unlink(missing_ok=True)


if __name__ == "__main__":
    fetch()
