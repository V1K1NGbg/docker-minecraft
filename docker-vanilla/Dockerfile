ARG java=25

FROM eclipse-temurin:${java}-jdk as build

RUN apt-get update -y && apt-get upgrade -y && apt-get install git wget jq -y \
    && git config --global core.autocrlf input

ARG version

ENV version=$version

# curl https://piston-meta.mojang.com/mc/game/version_manifest_v2.json
# for version

RUN wget -qO- "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json" \
    | jq -r --arg v "${version}" '.versions[] | select(.id == $v) | .url' \
    | xargs wget -qO- \
    | jq -r '.downloads.server.url' \
    | xargs wget -O "vanilla.jar"

######################################################################################

FROM eclipse-temurin:${java}-jdk

RUN apt-get update -y
RUN apt-get upgrade -y

COPY --from=build /vanilla.jar /

RUN mkdir -p /data \
    && adduser --disabled-password --gecos "" --home /home/minecraft minecraft \
    && chown -R minecraft /data /home/minecraft \
    && chmod -R 755 /data /home/minecraft && chmod 1777 /data

VOLUME ["/data"]

WORKDIR /data

USER minecraft

ARG flags=""

ENV min=1 \
    max=2 \
    JAVA_FLAGS="$flags" \
    SERVER_START="-jar /vanilla.jar" \
    SERVER_ARGS="nogui"

COPY start.sh /start.sh

CMD ["/start.sh"]

EXPOSE 25565
