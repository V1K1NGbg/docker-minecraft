FROM eclipse-temurin:21-jdk as build

RUN apt-get update -y && apt-get upgrade -y && apt-get install git wget -y
RUN git config --global core.autocrlf input

ARG version=3.1.1
ARG build=102

ENV version=$version
ENV build=$build

RUN wget "https://api.papermc.io/v2/projects/velocity/versions/${version}/builds/${build}/downloads/velocity-${version}-${build}.jar" -O "/velocity.jar"

######################################################################################

FROM eclipse-temurin:21-jdk

RUN apt-get update -y && apt-get upgrade -y

COPY --from=build /velocity.jar /

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
    && java "-Xms${min}G" "-Xmx${max}G" -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -jar /velocity.jar

EXPOSE 25577
