"""Shared helpers for the update.py / push.py scripts in every docker-* folder."""

import json
import os
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(ROOT, "logs")
REPO = "v1k1ngbg"
PUSH = os.environ.get("PUSH", "1") != "0"
RETRIES = 3


def getjson(url):
    req = urllib.request.Request(url, headers={"User-Agent": "docker-minecraft-updater"})
    return json.loads(urllib.request.urlopen(req).read())


def is_release(version):
    """True for plain releases like 1.21.11 or 26.1.2, false for pre/rc/snapshots."""
    return all(c.isdigit() or c == "." for c in version)


def vkey(version):
    """Sort key for release version strings."""
    return [int(x) for x in version.split(".")]


# Extra versions built besides the newest of each line (modpacks often stay on these), tagged
# with their full version (forge:1.20.1, vanilla:1.20.1); their build is still the newest one,
# fetched by update.py like the others. A version that does not exist upstream stops the update.
MANUAL = {
    "paper": [],
    "fabric": [],
    "forge": ["1.19.2", "1.20.1"],
    "vanilla": [],
    "velocity": [],  # e.g. "3.4.0-SNAPSHOT"
}


def manual(server, known):
    """This server's manual versions, each checked against the versions upstream offers."""
    unknown = [v for v in MANUAL.get(server, []) if v not in known]
    if unknown:
        raise SystemExit(server + ": unknown manual version(s) " + ", ".join(unknown) + " (common.MANUAL)")
    return list(MANUAL.get(server, []))


def with_manual(server, versions, known):
    """The newest of every line plus this server's manual versions, oldest first."""
    return sorted(set(newest_per_tag(versions)) | set(manual(server, known)), key=vkey)


def tag(version, server=None):
    """Docker tag for a Minecraft version: 1.21.11 -> 1.21, 26.3 -> 26; a manual version keeps its full version."""
    if version in MANUAL.get(server, []):
        return version
    parts = version.split(".")
    return parts[0] + "." + parts[1] if parts[0] == "1" else parts[0]


def java(version):
    """Java version (and Dockerfile suffix) used for a Minecraft version."""
    parts = version.split(".")
    if parts[0] != "1":
        return "25"  # year based versions (26.x and newer)
    minor = int(parts[1])
    patch = int(parts[2]) if len(parts) > 2 else 0
    # 1.20.5 moved to java 21; 1.20 - 1.20.4 still run on java 17
    if minor > 20 or (minor == 20 and patch >= 5):
        return "21"
    if minor == 20:
        return "17"
    elif minor >= 17:
        return "17"
    elif minor >= 13:
        return "11"
    return "8"


# PaperMC's recommended flags (Aikar's G1 flags), from https://fill.papermc.io/v3/projects/paper/versions/<version>
FLAGS = ("-XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:+ParallelRefProcEnabled -XX:+PerfDisableSharedMem "
         "-XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1HeapRegionSize=8M -XX:G1HeapWastePercent=5 "
         "-XX:G1MaxNewSizePercent=40 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 "
         "-XX:G1NewSizePercent=30 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:G1ReservePercent=20 "
         "-XX:InitiatingHeapOccupancyPercent=15 -XX:MaxGCPauseMillis=200 -XX:MaxTenuringThreshold=1 -XX:SurvivorRatio=32")

# what PaperMC recommends for java 25 (26.x): compact object headers, and the flags that are now defaults dropped
FLAGS_25 = ("-XX:+UseCompactObjectHeaders -XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:+PerfDisableSharedMem "
            "-XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1HeapRegionSize=8M -XX:G1MaxNewSizePercent=40 "
            "-XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1NewSizePercent=30 "
            "-XX:G1RSetUpdatingPauseTimePercent=5 -XX:G1ReservePercent=20 -XX:InitiatingHeapOccupancyPercent=15 "
            "-XX:MaxTenuringThreshold=1 -XX:SurvivorRatio=32")

# velocity's recommended proxy flags (https://docs.papermc.io/velocity/tuning)
FLAGS_PROXY = ("-XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions "
               "-XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch")


def jvm_flags(javaversion):
    """Recommended JVM flags for a java version (baked into the image, override with -e JAVA_FLAGS=...)."""
    return FLAGS_25 if int(javaversion) >= 25 else FLAGS


def newest_per_tag(versions):
    """Keep only the newest release for every docker tag, ordered oldest to newest."""
    newest = {}
    for v in versions:
        if is_release(v) and (tag(v) not in newest or vkey(v) > vkey(newest[tag(v)])):
            newest[tag(v)] = v
    return sorted(newest.values(), key=vkey)


def write_lines(folder, lines):
    with open(os.path.join(folder, "versionsandbuilds.txt"), "w") as f:
        f.write("\n".join(lines))


def read_lines(folder):
    with open(os.path.join(folder, "versionsandbuilds.txt")) as f:
        return [line.strip() for line in f if line.strip()]


def job(image, imagetag, folder, dockerfile="Dockerfile", args=None):
    return {"image": image, "tag": imagetag, "folder": folder, "dockerfile": dockerfile, "args": args or {}}


def run_update(folder):
    subprocess.run([sys.executable, os.path.join(folder, "update.py")], cwd=folder, check=True)


def _build_and_push(j):
    name = REPO + "/" + j["image"] + ":" + j["tag"]
    log = os.path.join(LOGS, j["image"] + "-" + j["tag"] + ".log")
    # built from the repo root so every image can COPY the shared start.sh (see .dockerignore)
    cmd = ["docker", "build", "--pull", "-t", name, "-f", os.path.join(j["folder"], j["dockerfile"])]
    for k, v in j["args"].items():
        cmd += ["--build-arg", k + "=" + v]
    cmd.append(ROOT)
    with open(log, "w") as out:
        # downloads (forge installer, mojang libraries) time out now and then, so retry a few times
        for attempt in range(1, RETRIES + 1):
            out.write("$ " + " ".join(cmd) + "  (attempt " + str(attempt) + ")\n")
            out.flush()
            ok = subprocess.run(cmd, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT).returncode == 0
            if ok and PUSH:
                ok = subprocess.run(["docker", "push", name], stdout=out, stderr=subprocess.STDOUT).returncode == 0
            if ok:
                break
    return name, ok, log


def run_jobs(jobs, workers=None):
    """Build and push all jobs in parallel. Returns True when every job succeeded."""
    os.makedirs(LOGS, exist_ok=True)
    workers = workers or int(os.environ.get("JOBS", max(2, (os.cpu_count() or 4) // 3)))
    print("Building " + str(len(jobs)) + " images with " + str(workers) + " parallel jobs, logs in " + LOGS)
    failed = []
    with ThreadPoolExecutor(workers) as pool:
        for fut in as_completed([pool.submit(_build_and_push, j) for j in jobs]):
            name, ok, log = fut.result()
            print(("OK    " if ok else "FAIL  ") + name + ("" if ok else "  (see " + log + ")"), flush=True)
            if not ok:
                failed.append(name)
    print(str(len(jobs) - len(failed)) + "/" + str(len(jobs)) + " images built" + (" and pushed" if PUSH else ""))
    for name in failed:
        print("  failed: " + name)
    return not failed
