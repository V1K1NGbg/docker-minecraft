import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))

# versionsandbuilds.txt: 3 lines per docker tag, oldest first: version / build / java

API = "https://fill.papermc.io/v3/projects/paper"

allversions = [v for family in getjson(API)["versions"].values() for v in family]

lines = []

for version in with_manual("paper", allversions, allversions):
    build = getjson(API + "/versions/" + version + "/builds/latest")["id"]
    lines += [version, str(build), java(version)]

write_lines(FOLDER, lines)

print("Paper update complete!")
