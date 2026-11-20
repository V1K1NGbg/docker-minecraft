import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))

# versionsandbuilds.txt: installer / loader, then 2 lines per docker tag, oldest first: version / java

API = "https://meta.fabricmc.net/v2/versions"

lines = [getjson(API + "/installer")[0]["version"], getjson(API + "/loader")[0]["version"]]

for version in newest_per_tag([v["version"] for v in getjson(API + "/game") if v["stable"]]):
    lines += [version, java(version)]

write_lines(FOLDER, lines)

print("Fabric update complete!")
