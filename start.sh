#!/bin/sh
# If /data/launch-server.sh exists it is run as-is.
# Otherwise the server is started directly with the recommended java flags.
#
#   min / max      heap size in GB (default 1 / 2)
#   JAVA_FLAGS     JVM flags (default: recommended flags for this java version)
#   SERVER_START   what to start, e.g. "-jar /paper.jar"
#   SERVER_ARGS    arguments for the server (default "nogui")

cd /data

for dir in /plugins /mods; do
    [ -d "$dir" ] && ln -sf "$dir" /data/
done

echo 'eula=TRUE' > eula.txt

if [ -f ./launch-server.sh ]; then
    exec bash ./launch-server.sh
fi

exec java -Xms${min}G -Xmx${max}G $JAVA_FLAGS $SERVER_START $SERVER_ARGS
