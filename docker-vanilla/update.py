import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))

# versionsandbuilds.txt: 2 lines per version: the latest release first, then the manual versions
# (common.MANUAL), each: version / java

manifest = getjson("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")
urls = {v["id"]: v["url"] for v in manifest["versions"] if v["type"] == "release"}

lines = []
for version in [manifest["latest"]["release"]] + manual("vanilla", urls):
    lines += [version, str(getjson(urls[version])["javaVersion"]["majorVersion"])]

write_lines(FOLDER, lines)

print("Vanilla update complete!")
