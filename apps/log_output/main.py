from datetime import UTC, datetime
from time import sleep
from uuid import uuid4


def main() -> None:
    startup_string = uuid4()
    while True:
        print(f"{datetime.now(UTC)}: {startup_string}")
        sleep(5)


if __name__ == "__main__":
    main()
