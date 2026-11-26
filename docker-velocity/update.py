import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))

# versionsandbuilds.txt: latest release version / build / latest snapshot version / build, then
# version / build for each manual version (common.MANUAL)

API = "https://fill.papermc.io/v3/projects/velocity"


def key(version):
    return vkey(version.split("-")[0])


def build(version):
    return str(getjson(API + "/versions/" + version + "/builds/latest")["id"])


allversions = [v for family in getjson(API)["versions"].values() for v in family]

release = max([v for v in allversions if not v.endswith("SNAPSHOT")], key=key)
snapshot = max([v for v in allversions if v.endswith("SNAPSHOT")], key=key)

lines = [release, build(release), snapshot, build(snapshot)]
for version in manual("velocity", allversions):
    lines += [version, build(version)]

write_lines(FOLDER, lines)

print("Velocity update complete!")
