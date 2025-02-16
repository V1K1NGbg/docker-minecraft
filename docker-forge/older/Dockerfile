FROM eclipse-temurin:8-jdk as build

RUN apt-get update -y && apt-get upgrade -y && apt-get install git wget -y \
    && git config --global core.autocrlf input

ARG version=1.12.2
ARG build=14.23.5.2859
ARG long_file=""

ENV version=$version
ENV build=$build
ENV long_file=$long_file

# curl https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json
# for version and builds

RUN wget "https://maven.minecraftforge.net/net/minecraftforge/forge/${version}-${build}${long_file}/forge-${version}-${build}${long_file}-installer.jar" -O "forge.jar" \
    && java -jar forge.jar --installServer \
    && rm forge.jar* \
    && [ -e forge*.jar ] && mv forge*.jar forge.jar || echo "no forge"

######################################################################################

FROM eclipse-temurin:8-jdk

RUN apt-get update -y && apt-get upgrade -y

RUN mkdir -p /data \
    && mkdir -p /mods

COPY --from=build /run.sh* /user_jvm_args.txt* /forge.jar* /minecraft*.jar /
COPY --from=build /libraries /libraries

RUN adduser --disabled-password --gecos "" --home /home/minecraft minecraft \
    && chown -R minecraft /data /mods /home/minecraft \
    && chmod -R 755 /data /home/minecraft

VOLUME ["/data","/mods"]

WORKDIR /data

USER minecraft

ENV min=1
ENV max=2

CMD ln -sf /mods /data/ \
    && echo 'eula=TRUE' >| eula.txt \
    && ls -a \
    # && java -version \
    && [ -e /run.sh ] && (echo "-Xms${min}G" "-Xmx${max}G" >| user_jvm_args.txt && /run.sh) || java -server "-Xms${min}G" "-Xmx${max}G" -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=40 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -jar /forge.jar nogui

EXPOSE 25565