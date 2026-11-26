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

## Building

```sh
python3 push.py                 # update versions, build and push everything in parallel
python3 push.py paper forge     # only some servers
JOBS=8 PUSH=0 python3 push.py   # 8 parallel builds, don't push
```

Per-build logs end up in `logs/`.
