import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))


def jobs():
    run_update(FOLDER)
    l = read_lines(FOLDER)
    return [job("paper", tag(l[i], "paper"), FOLDER, "Dockerfile" + l[i + 2], {"version": l[i], "build": l[i + 1], "flags": jvm_flags(l[i + 2])})
            for i in range(0, len(l), 3)]


if __name__ == "__main__":
    sys.exit(0 if run_jobs(jobs()) else 1)
