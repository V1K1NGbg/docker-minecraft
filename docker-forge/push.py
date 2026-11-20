import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))


def long_file(version):
    # forge builds for 1.7 - 1.9 have the minecraft version appended to the file name
    return "-" + version if version.split(".")[0] == "1" and int(version.split(".")[1]) < 10 else ""


def start(version, build):
    # forge 1.17+ has no single server jar, it is started from the argument file the installer writes
    parts = version.split(".")
    if parts[0] == "1" and int(parts[1]) < 17:
        return "-jar /data/forge.jar"
    return "@libraries/net/minecraftforge/forge/" + version + "-" + build + "/unix_args.txt"


def jobs():
    run_update(FOLDER)
    l = read_lines(FOLDER)
    return [job("forge", tag(l[i]), FOLDER, "Dockerfile" + l[i + 2],
                {"version": l[i], "build": l[i + 1], "long_file": long_file(l[i]), "start": start(l[i], l[i + 1]), "flags": jvm_flags(l[i + 2])})
            for i in range(0, len(l), 3)]


if __name__ == "__main__":
    sys.exit(0 if run_jobs(jobs()) else 1)
