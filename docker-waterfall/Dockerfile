FROM eclipse-temurin:17-jdk as build

RUN apt-get update -y && apt-get upgrade -y && apt-get install git wget -y
RUN git config --global core.autocrlf input

ARG version=1.19
ARG build=506

ENV version=$version
ENV build=$build

RUN wget "https://papermc.io/api/v2/projects/waterfall/versions/${version}/builds/${build}/downloads/waterfall-${version}-${build}.jar" -O "/waterfall.jar"

######################################################################################

FROM eclipse-temurin:17-jdk

RUN apt-get update -y
RUN apt-get upgrade -y

COPY --from=build /waterfall.jar /

RUN mkdir -p /data \
    && mkdir -p /plugins \
    && adduser --disabled-password --gecos "" --home /home/minecraft minecraft \
    && chown -R minecraft /data /plugins /home/minecraft \
    && chmod -R 755 /data /home/minecraft

VOLUME ["/data","/plugins"]

WORKDIR /data

USER minecraft

ENV min=1
ENV max=2

CMD ln -sf /plugins /data/ \
    && echo "eula=TRUE" > eula.txt \
    && java "-Xms${min}G" "-Xmx${max}G" -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -jar /waterfall.jar

EXPOSE 25577
