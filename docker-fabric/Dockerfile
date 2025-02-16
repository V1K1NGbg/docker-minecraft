FROM eclipse-temurin:17-jdk as build

RUN apt-get update -y && apt-get upgrade -y && apt-get install git wget -y \
    && git config --global core.autocrlf input

ARG version=1.21.4
ARG loader=0.16.10
ARG installer=1.0.1

ENV version=$version
ENV loader=$loader
ENV installer=$installer

# curl https://meta.fabricmc.net/v2/versions/game
# for version

# curl https://meta.fabricmc.net/v2/versions/loader
# for loader

# curl https://meta.fabricmc.net/v2/versions/installer
# for installer

RUN wget "https://meta.fabricmc.net/v2/versions/loader/${version}/${loader}/${installer}/server/jar" -O "fabric.jar"

######################################################################################

FROM eclipse-temurin:17-jdk

RUN apt-get update -y && apt-get upgrade -y

COPY --from=build /fabric.jar /

RUN mkdir -p /data \
    && mkdir -p /mods \
    && adduser --disabled-password --gecos "" --home /home/minecraft minecraft \
    && chown -R minecraft /data /mods /home/minecraft \
    && chmod -R 755 /data /home/minecraft

VOLUME ["/data","/mods"]

WORKDIR /data

USER minecraft

ENV min=1
ENV max=2

CMD ln -sf /mods /data/ \
    && echo 'eula=TRUE' > eula.txt \
    && java "-Xms${min}G" "-Xmx${max}G" -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=40 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -jar /fabric.jar nogui

EXPOSE 25565
