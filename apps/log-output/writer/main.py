from datetime import UTC, datetime
from pathlib import Path
from time import sleep
from uuid import uuid4

OUTPUT_DIR = Path("./files/")
OUTPUT_FILE = Path(OUTPUT_DIR / "output")


def main() -> None:
    startup_string = uuid4()
    OUTPUT_DIR.mkdir(exist_ok=True)

    while True:
        with open(OUTPUT_FILE, "w") as f:
            f.write(f"{datetime.now(UTC)}: {startup_string}")
        sleep(5)


if __name__ == "__main__":
    main()
