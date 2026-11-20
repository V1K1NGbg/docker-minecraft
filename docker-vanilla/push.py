import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))


def jobs():
    run_update(FOLDER)
    l = read_lines(FOLDER)
    return [job("vanilla", "latest", FOLDER, args={"version": l[0], "java": l[1], "flags": jvm_flags(l[1])})]


if __name__ == "__main__":
    sys.exit(0 if run_jobs(jobs()) else 1)
