import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import *

FOLDER = os.path.dirname(os.path.abspath(__file__))

# versionsandbuilds.txt: latest release version / java

manifest = getjson("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")
version = manifest["latest"]["release"]
url = [v["url"] for v in manifest["versions"] if v["id"] == version][0]

write_lines(FOLDER, [version, str(getjson(url)["javaVersion"]["majorVersion"])])

print("Vanilla update complete!")
