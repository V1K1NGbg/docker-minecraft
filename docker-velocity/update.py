import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))

# versionsandbuilds.txt: latest release version / build / latest snapshot version / build

API = "https://fill.papermc.io/v3/projects/velocity"


def key(version):
    return vkey(version.split("-")[0])


def build(version):
    return str(getjson(API + "/versions/" + version + "/builds/latest")["id"])


allversions = [v for family in getjson(API)["versions"].values() for v in family]

release = max([v for v in allversions if not v.endswith("SNAPSHOT")], key=key)
snapshot = max([v for v in allversions if v.endswith("SNAPSHOT")], key=key)

write_lines(FOLDER, [release, build(release), snapshot, build(snapshot)])

print("Velocity update complete!")
