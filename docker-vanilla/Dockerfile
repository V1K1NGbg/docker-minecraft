FROM eclipse-temurin:21-jdk as build

RUN apt-get update -y && apt-get upgrade -y && apt-get install git wget -y \
    && git config --global core.autocrlf input

# 1.21.4
RUN wget "https://piston-data.mojang.com/v1/objects/4707d00eb834b446575d89a61a11b5d548d8c001/server.jar" -O "vanilla.jar"

######################################################################################

FROM eclipse-temurin:21-jdk

RUN apt-get update -y
RUN apt-get upgrade -y

COPY --from=build /vanilla.jar /

RUN mkdir -p /data \
    && adduser --disabled-password --gecos "" --home /home/minecraft minecraft \
    && chown -R minecraft /data /home/minecraft \
    && chmod -R 755 /data /home/minecraft

VOLUME ["/data"]

WORKDIR /data

USER minecraft

ENV min=1
ENV max=2

CMD ln -sf /data/ \
    && echo 'eula=TRUE' > eula.txt \
    && java "-Xms${min}G" "-Xmx${max}G" -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar /vanilla.jar nogui

EXPOSE 25565
