import importlib.util
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, run_jobs

# usage: python3 push.py [paper fabric forge velocity vanilla]   (default: all)
#        JOBS=8 python3 push.py                                     (number of parallel builds)
#        PUSH=0 python3 push.py                                     (build only, don't push)

SERVERS = ["paper", "fabric", "forge", "velocity", "vanilla"]  # waterfall is deprecated


def load_jobs(server):
    path = os.path.join(ROOT, "docker-" + server, "push.py")
    spec = importlib.util.spec_from_file_location("push_" + server, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.jobs()


servers = sys.argv[1:] or SERVERS

os.system('docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -aq)')
subprocess.run(["docker", "container", "prune", "-f"])
subprocess.run(["docker", "image", "prune", "-f"])

# run all update.py scripts in parallel, then build everything in one shared pool
with ThreadPoolExecutor(len(servers)) as pool:
    jobs = [j for js in pool.map(load_jobs, servers) for j in js]

ok = run_jobs(jobs)

subprocess.run(["docker", "image", "prune", "-f"])

# os.system('cd Discord-bot && docker build -t v1k1ngbg/discord-bot ./Discord-bot/ && docker push v1k1ngbg/discord-bot && cd ..')
# os.system('docker run -d --restart=always -v ~/server/config.json:/usr/bot/config/config.json -v /var/run/docker.sock:/var/run/docker.sock --name discord-bot v1k1ngbg/discord-bot:latest')

sys.exit(0 if ok else 1)
