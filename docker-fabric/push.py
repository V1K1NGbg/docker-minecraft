import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))


def jobs():
    run_update(FOLDER)
    l = read_lines(FOLDER)
    return [job("fabric", tag(l[i]), FOLDER, "Dockerfile" + l[i + 1],
                {"version": l[i], "loader": l[1], "installer": l[0], "flags": jvm_flags(l[i + 1])})
            for i in range(2, len(l), 2)]


if __name__ == "__main__":
    sys.exit(0 if run_jobs(jobs()) else 1)
