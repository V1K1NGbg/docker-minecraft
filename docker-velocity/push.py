import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))


def jobs():
    run_update(FOLDER)
    l = read_lines(FOLDER)
    return [job("velocity", l[0].split(".")[0], FOLDER, args={"version": l[0], "build": l[1], "flags": FLAGS_PROXY}),
            job("velocity", l[2].split(".")[0] + "S", FOLDER, args={"version": l[2], "build": l[3], "flags": FLAGS_PROXY})] + \
           [job("velocity", l[i], FOLDER, args={"version": l[i], "build": l[i + 1], "flags": FLAGS_PROXY}) for i in range(4, len(l), 2)]


if __name__ == "__main__":
    sys.exit(0 if run_jobs(jobs()) else 1)
