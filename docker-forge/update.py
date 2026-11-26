import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))

# versionsandbuilds.txt: 3 lines per docker tag, oldest first: minecraft version / forge build / java

promos = getjson("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json")["promos"]

recommended = [k.rsplit("-", 1)[0] for k in promos if k.endswith("-recommended")]
recommended = [v for v in recommended if is_release(v) and vkey(v) >= [1, 7]]

lines = []

# the newest of every line, plus the manual versions (common.MANUAL), each with its newest recommended
# build (or the newest build when there is no recommended one yet)
known = {k.rsplit("-", 1)[0] for k in promos}
versions = with_manual("forge", recommended, known)

for version in versions:
    build = promos.get(version + "-recommended") or promos[version + "-latest"]
    # forge 1.13 / 1.14 crash on java 11 (UnsupportedOperationException on launch), they need java 8
    lines += [version, build, "8" if tag(version) in ("1.13", "1.14") else java(version)]

write_lines(FOLDER, lines)

print("Forge update complete!")
