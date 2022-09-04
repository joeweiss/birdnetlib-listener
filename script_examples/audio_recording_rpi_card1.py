# This example requires arecord, which is available on most Linux systems.
# Record to 15 second files with arecord, then analyze with two analyzers.

from subprocess import Popen
import sys
import signal


def main():
    recording_dir = "audio/inbox"
    duration_secs = 15

    arecord_command_list = [
        "arecord",
        "-f",
        "S16_LE",
        "-c2",
        "-r48000",
        "-t",
        "wav",
        # "--device",
        # "hw:1,0",
        "--max-file-time",
        f"{duration_secs}",
        "--use-strftime",
        f"{recording_dir}/%F-%H:%M:%S.wav",
    ]

    recording_process = Popen(arecord_command_list)

    def signal_handler(sig, frame):
        recording_process.terminate()
        # Add error callbacks here if needed ...
        print("Gracefully exitting process ...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    recording_process.wait()

    try:
        recording_process.wait()
    except Exception as e:
        print("Exception")
        print(e)


if __name__ == "__main__":
    main()
