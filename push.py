import importlib.util
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, run_jobs

# usage: python3 push.py [paper fabric forge velocity vanilla]   (default: all)
#        python3 push.py forge:1.20.1 paper:26                      (only these docker tags)
#        JOBS=8 python3 push.py                                     (number of parallel builds)
#        PUSH=0 python3 push.py                                     (build only, don't push)
#        CLEAN=1 python3 push.py                                    (first stop and remove ALL docker
#                                                                    containers and images on this machine)

SERVERS = ["paper", "fabric", "forge", "velocity", "vanilla"]  # waterfall is deprecated


def load_jobs(server):
    path = os.path.join(ROOT, "docker-" + server, "push.py")
    spec = importlib.util.spec_from_file_location("push_" + server, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.jobs()


# "forge" builds every forge tag, "forge:1.20.1" only that one
wanted = {}
for arg in sys.argv[1:] or SERVERS:
    server, _, tag = arg.partition(":")
    if server not in SERVERS:
        sys.exit("unknown server '" + server + "' (one of " + ", ".join(SERVERS) + ")")
    if tag:
        wanted.setdefault(server, set())
        if wanted[server] is not None:
            wanted[server].add(tag)
    else:
        wanted[server] = None  # all tags

if os.environ.get("CLEAN") == "1":
    os.system('docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -aq)')
    subprocess.run(["docker", "container", "prune", "-f"])
subprocess.run(["docker", "image", "prune", "-f"])

# run the update.py scripts in parallel, then build the chosen tags in one shared pool
servers = list(wanted)
with ThreadPoolExecutor(len(servers)) as pool:
    jobs = [j for js in pool.map(load_jobs, servers) for j in js]
jobs = [j for j in jobs if wanted[j["image"]] is None or j["tag"] in wanted[j["image"]]]

missing = [s + ":" + t for s, tags in wanted.items() if tags for t in tags - {j["tag"] for j in jobs if j["image"] == s}]
if missing:
    sys.exit("no such tag: " + ", ".join(sorted(missing)))

ok = run_jobs(jobs)

subprocess.run(["docker", "image", "prune", "-f"])

# os.system('cd Discord-bot && docker build -t v1k1ngbg/discord-bot ./Discord-bot/ && docker push v1k1ngbg/discord-bot && cd ..')
# os.system('docker run -d --restart=always -v ~/server/config.json:/usr/bot/config/config.json -v /var/run/docker.sock:/var/run/docker.sock --name discord-bot v1k1ngbg/discord-bot:latest')

sys.exit(0 if ok else 1)
