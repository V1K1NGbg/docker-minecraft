#!/bin/sh
# If /data/launch-server.sh exists it is run as-is.
# Otherwise the server is started directly with the recommended java flags.
#
#   min / max      heap size in GB (default 1 / 2)
#   JAVA_FLAGS     JVM flags (default: recommended flags for this java version)
#   SERVER_START   what to start, e.g. "-jar /paper.jar"
#   SERVER_ARGS    arguments for the server (default "nogui")
#   LINK_DIRS      1 (default): /plugins and /mods are linked into /data.
#                  0: they are folders inside /data instead (kept with the world), and
#                  whatever the image ships in /plugins or /mods is copied in once.

cd /data

# Server files the image installs (Forge) live in /opt/server and are copied into /data
# on every start, so a fresh or reused volume always holds the image's server.
# user_jvm_args.txt is yours to edit and only copied when it is missing.
if [ -d /opt/server ]; then
    for file in /opt/server/*; do
        name=$(basename "$file")
        [ "$name" = user_jvm_args.txt ] && [ -e "$name" ] && continue
        cp -rf "$file" .
    done
fi

for dir in /plugins /mods; do
    [ -d "$dir" ] || continue
    if [ "${LINK_DIRS:-1}" = 0 ]; then
        name=$(basename "$dir")
        if [ ! -e "$name" ] && [ ! -L "$name" ]; then
            mkdir "$name" && cp -r "$dir"/. "$name"/ 2>/dev/null || true
        fi
    else
        ln -sf "$dir" /data/
    fi
done

echo 'eula=TRUE' > eula.txt

if [ -f ./launch-server.sh ]; then
    exec bash ./launch-server.sh
fi

exec java -Xms${min}G -Xmx${max}G $JAVA_FLAGS $SERVER_START $SERVER_ARGS
