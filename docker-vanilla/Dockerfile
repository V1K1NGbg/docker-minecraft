FROM eclipse-temurin:21-jdk as build

RUN apt-get update -y && apt-get upgrade -y && apt-get install git wget -y \
    && git config --global core.autocrlf input

# 1.21.4
RUN wget "https://piston-data.mojang.com/v1/objects/e6ec2f64e6080b9b5d9b471b291c33cc7f509733/server.jar" -O "vanilla.jar"

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
    && java "-Xms${min}G" "-Xmx${max}G" -jar /vanilla.jar nogui

EXPOSE 25565
