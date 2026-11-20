# Minecraft servers running in docker containers 

## Currently supported servers:
- [PaperMC](https://papermc.io/)
- [Forge](https://files.minecraftforge.net/)
- [Fabric](https://fabricmc.net/)
- [Velocity](https://velocitypowered.com/)
- [Vanilla](https://www.minecraft.net/)
- [Waterfall](https://papermc.io/) (Deprecated)

## Running

```sh
docker run -d -p 25565:25565 -v mc-data:/data -e min=2 -e max=6 v1k1ngbg/paper:26
```

Tags are the Minecraft version line (`1.8` … `1.21`, `26` for the newest 26.x), `velocity:4` / `velocity:4S` (snapshot) and `vanilla:latest`.

If `/data/launch-server.sh` exists it is run as-is (e.g. a modpack start script). Otherwise the server is started directly with the recommended Java flags:

| Variable | Default | |
|---|---|---|
| `min` / `max` | `1` / `2` | heap size in GB |
| `JAVA_FLAGS` | PaperMC's recommended flags for the image's Java version | set to `""` to run without them |
| `SERVER_ARGS` | `nogui` | arguments for the server |

## Building

```sh
python3 push.py                 # update versions, build and push everything in parallel
python3 push.py paper forge     # only some servers
JOBS=8 PUSH=0 python3 push.py   # 8 parallel builds, don't push
```

Per-build logs end up in `logs/`.
