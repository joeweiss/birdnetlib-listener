# Requires sox and pysox: install with:
#  brew install sox
#  pip install sox

import sox
from datetime import datetime


def main():

    duration_secs = 15
    output_directory = "audio/inbox"

    while True:
        filename = datetime.now().strftime("%Y-%m-%d-%H:%M:%S.wav")
        print(f"{output_directory}/{filename}")
        args = [
            "-d",
            "-t",
            "wav",
            f"{output_directory}/{filename}",
            "trim",
            "0",
            f"{duration_secs}",
        ]
        sox.core.sox(args)


if __name__ == "__main__":
    main()
